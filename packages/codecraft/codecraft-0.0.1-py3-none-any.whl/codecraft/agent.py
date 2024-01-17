import json
from typing import List

from langchain.callbacks import get_openai_callback
from langchain.chat_models.base import BaseChatModel
from langchain.schema import BaseMessage, FunctionMessage, HumanMessage, SystemMessage
from langchain.tools import format_tool_to_openai_function
from termcolor import cprint
from yaspin import yaspin

from codecraft.prompts import SYSTEM_PROMPT


class Agent:
    llm: BaseChatModel
    messages: List
    tools: dict
    max_rounds: int

    def __init__(self, llm: BaseChatModel, tools: List):
        self.llm = llm
        self.messages = [SystemMessage(content=SYSTEM_PROMPT)]
        self.tools = {it.name: it for it in tools}
        self.max_rounds = 24

    @property
    def functions(self) -> List[dict]:
        return [dict(format_tool_to_openai_function(t)) for t in self.tools.values()]

    def reset_history(self, user_msg=None):
        self.messages = [SystemMessage(content=SYSTEM_PROMPT)]
        cprint(f"{SYSTEM_PROMPT}", "light_blue")
        if user_msg is not None:
            self.messages.append(HumanMessage(content=user_msg))
            cprint(f"{user_msg}", "blue")
        return self.messages

    def run(self, user_msg: str):
        messages = self.reset_history(user_msg)
        response = "Done"
        left_rounds = self.max_rounds
        with get_openai_callback() as cb:
            try:
                while left_rounds > 0:
                    left_rounds -= 1
                    response = self.next_step()
                    if "FINAL ANSWER" in response:
                        cprint(f"💵 Cost: $ {cb.total_cost:.4}\n", "green")
                        break
                if left_rounds == 0:
                    cprint(f"💵 Cost: $ {cb.total_cost:.4}\n", "green")
            except KeyboardInterrupt:
                cprint(f"💵 Cost: $ {cb.total_cost:.4}\n", "green")
        return response, messages

    def parse_ai_message(self, ai_message: BaseMessage):
        function_call = ai_message.additional_kwargs.get("function_call", {})
        if function_call:
            function_name = function_call["name"]
            arguments = json.loads(function_call["arguments"])
            return ai_message, function_name, arguments
        return ai_message, None, None

    def next_step(self):
        with yaspin(text="Calling LLM "):
            ai_message = self.llm(self.messages, functions=self.functions)
        self.messages.append(ai_message)
        cprint(f"\n🤖: {ai_message.content or 'Calling tool'}\n", "yellow")
        ai_message, function_name, arguments = self.parse_ai_message(ai_message)
        if function_name and arguments:
            if function_name == "diff":
                cprint(
                    f"🧰 {arguments['commit_message']}\n"
                    f"{arguments['filename']}\n"
                    f"<<<<<<< ORIGINAL\n"
                    f"{arguments['original']}\n"
                    f"=======\n"
                    f"{arguments['updated']}\n"
                    f">>>>>>> UPDATED\n",
                    "light_green",
                )
            else:
                cprint(f"🧰 [{function_name}]\n{json.dumps(arguments, indent=4)}\n", "light_green")
            with yaspin(text="Running tool "):
                next_action_result = self.tools[function_name](arguments)
            if next_action_result.startswith("Error:"):
                cprint(f"🤦 {next_action_result}\n", "red")
            else:
                cprint(f"✅ {next_action_result}\n", "green")
            self.messages.append(FunctionMessage(name=function_name, content=next_action_result))
        return ai_message.content
