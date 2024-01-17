from functools import partial

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.tools import MoveFileTool
from prompt_toolkit import prompt
from prompt_toolkit.cursor_shapes import CursorShape

from codecraft.agent import Agent
from codecraft.completer import AutoCompleter
from codecraft.conf import MODEL_NAME
from codecraft.prompts import (
    COVERAGE_INSTRUCTION,
    DEV_INSTRUCTIONS,
)
from codecraft.repomap import get_repomap
from codecraft.tools.context import add_file_to_context_tool
from codecraft.tools.diff import diff_tool, git_commit_tool
from codecraft.tools.pytest import run_test_tool

from .context import context

load_dotenv("../.env")

# add current folder to sys path

import langchain

langchain.verbose = True


def load_files_content(filenames):
    return "\n\n".join([f"file {filename}:\n```\n{load_file_content(filename)}\n```" for filename in filenames])


def load_file_content(path):
    with open(path, "r") as f:
        return f.read()


tools = [
    git_commit_tool,
    diff_tool,
    MoveFileTool(),
    add_file_to_context_tool,
    run_test_tool,
]

COMMAND_ADD = "add"
COMMAND_PROMPT = "prompt"
COMMAND_CLEAR = "clear"

COMMANDS = [COMMAND_ADD, COMMAND_PROMPT, COMMAND_CLEAR]


def is_command(query):
    if query.startswith("/"):
        cmd, _ = extract_cmd(query)
        if cmd in COMMANDS:
            return True
    return False


def extract_cmd(query):
    splitted = query.split("/", maxsplit=1)[1].split(" ", maxsplit=1)
    if len(splitted) == 1:
        return splitted[0], ""
    return splitted


def apply_command(query, files):
    cmd, params = extract_cmd(query)
    if cmd == COMMAND_ADD:
        print(f"Added {params} files to context")
        return [*files, params]
    if cmd == COMMAND_PROMPT:
        print(get_dev_prompt(files, query))
        return files
    if cmd == COMMAND_CLEAR:
        return []


def get_prompt(instructions, files, query=None, show_repomap=True):
    source_code = f"\n\nSource code:\n{load_files_content(set(files))}" if files else ""

    repomap = get_repomap()

    user_message_prefix_prompt = (
        (f"\n\nREPOSITORY STRUCTURE:\n{repomap}\n" + source_code + instructions) if show_repomap else ""
    )
    if query is None:
        return user_message_prefix_prompt

    return f"{user_message_prefix_prompt}\n\nUser: {query}\n"


get_dev_prompt = partial(get_prompt, DEV_INSTRUCTIONS)
get_coverage_prompt = partial(get_prompt, COVERAGE_INSTRUCTION)


def run_session(coverage=False, query=None):
    llm = ChatOpenAI(temperature=0, model_name=MODEL_NAME, model_kwargs={"seed": 42})

    agent = Agent(llm=llm, tools=tools)

    context.added_files = []

    if coverage:
        response = agent.run(get_coverage_prompt(context.added_files))
        return response

    files, names = get_repomap(files_and_names=True)
    autocompleter = AutoCompleter(files, names, COMMANDS)
    print()  # to have margin in shell
    if query is not None:
        response = agent.run(get_dev_prompt(context.added_files, query))
        return response
    else:
        while True:
            query = prompt(
                "> ",
                cursor=CursorShape.BLINKING_UNDERLINE,
                completer=autocompleter,
            )

            if is_command(query):
                context.added_files = apply_command(query, context.added_files)
                continue

            response = agent.run(get_dev_prompt(context.added_files, query))
            if response is None:
                break


if __name__ == "__main__":  # pragma: no cover
    run_session()
