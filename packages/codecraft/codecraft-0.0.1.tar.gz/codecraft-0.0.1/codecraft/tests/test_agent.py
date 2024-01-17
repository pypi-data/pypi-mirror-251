import json
from unittest.mock import MagicMock, patch

from langchain.chat_models.base import BaseChatModel
from langchain.schema import AIMessage, BaseMessage, HumanMessage, SystemMessage

from codecraft.agent import Agent


def test_agent_reset_history():
    llm = MagicMock(spec=BaseChatModel)
    tools = []
    agent = Agent(llm, tools)
    user_msg = "Hello, world!"
    messages = agent.reset_history(user_msg)
    assert len(messages) == 2
    assert isinstance(messages[0], SystemMessage)
    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == user_msg


def test_agent_parse_ai_message():
    llm = MagicMock(spec=BaseChatModel)
    tools = []
    agent = Agent(llm, tools)
    ai_message = AIMessage(
        content="Hello, world!",
        additional_kwargs={"function_call": {"name": "test", "arguments": json.dumps({"key": "value"})}},
    )
    parsed_message, function_name, arguments = agent.parse_ai_message(ai_message)
    assert parsed_message == ai_message
    assert function_name == "test"
    assert arguments == {"key": "value"}


def test_agent_run():
    llm = MagicMock(spec=BaseChatModel)
    llm.return_value = AIMessage(content="FINAL ANSWER", additional_kwargs={})
    tool = MagicMock()
    tool.name = "test"
    tool.return_value = "Done"
    tools = [tool]
    agent = Agent(llm, tools)
    user_msg = "Run the agent"
    with patch("codecraft.agent.cprint"), patch("codecraft.agent.get_openai_callback") as mock_callback:
        mock_callback.return_value.__enter__.return_value.total_cost = 0.0
        response, messages = agent.run(user_msg)
    assert response == "FINAL ANSWER"
    assert len(messages) == 3
    assert isinstance(messages[0], SystemMessage)
    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == user_msg


def test_agent_next_step_error_handling():
    llm = MagicMock(spec=BaseChatModel)
    llm.return_value = AIMessage(
        content="Run tool",
        additional_kwargs={"function_call": {"name": "test", "arguments": json.dumps({"key": "value"})}},
    )
    tool = MagicMock()
    tool.name = "test"
    tool.return_value = "Error: Something went wrong"
    tools = [tool]
    agent = Agent(llm, tools)
    with patch("codecraft.agent.cprint") as mock_cprint:
        response = agent.next_step()
    assert response == "Run tool"
    assert len(agent.messages) == 3
    assert isinstance(agent.messages[1], BaseMessage)
    assert agent.messages[1].content == "Run tool"
    mock_cprint.assert_called_with("🤦 Error: Something went wrong\n", "red")


def test_agent_next_step_diff_tool_call():
    llm = MagicMock(spec=BaseChatModel)
    llm.return_value = AIMessage(
        content="Hello, world!",
        additional_kwargs={
            "function_call": {
                "name": "diff",
                "arguments": json.dumps(
                    {
                        "filename": "test.py",
                        "original": "original",
                        "updated": "updated",
                        "commit_message": "Update test.py",
                    }
                ),
            }
        },
    )
    tool = MagicMock()
    tool.name = "diff"
    tool.return_value = "Done"
    tools = [tool]
    agent = Agent(llm, tools)
    with patch("codecraft.agent.cprint") as mock_cprint:
        response = agent.next_step()
    assert response == "Hello, world!"
    assert len(agent.messages) == 3
    assert isinstance(agent.messages[1], BaseMessage)
    assert agent.messages[1].content == "Hello, world!"
    assert mock_cprint.mock_calls[1].args == (
        "🧰 Update test.py\n" "test.py\n" "<<<<<<< ORIGINAL\n" "original\n" "=======\n" "updated\n" ">>>>>>> UPDATED\n",
        "light_green",
    )


def test_agent_diff():
    llm = MagicMock(spec=BaseChatModel)
    llm.return_value = AIMessage(
        content="Hello, world!",
        additional_kwargs={"function_call": {"name": "test", "arguments": json.dumps({"key": "value"})}},
    )
    tool = MagicMock()
    tool.name = "test"
    tool.return_value = "Done"
    tools = [tool]
    agent = Agent(llm, tools)
    with patch("codecraft.agent.cprint"):
        response = agent.next_step()
    assert response == "Hello, world!"
    assert len(agent.messages) == 3
    assert isinstance(agent.messages[1], BaseMessage)
    assert agent.messages[1].content == "Hello, world!"


def test_agent_run_max_rounds():
    llm = MagicMock(spec=BaseChatModel)
    llm.return_value = AIMessage(content="Some response", additional_kwargs={})
    tool = MagicMock()
    tool.name = "test"
    tool.return_value = "Done"
    tools = [tool]
    agent = Agent(llm, tools)
    agent.max_rounds = 1  # Set max_rounds to 1 to trigger the condition quickly
    user_msg = "Run the agent until max rounds"
    with patch("codecraft.agent.cprint") as mock_cprint, patch("codecraft.agent.get_openai_callback") as mock_callback:
        mock_callback.return_value.__enter__.return_value.total_cost = 0.1234
        response, messages = agent.run(user_msg)
    assert response == "Some response"
    assert len(messages) == 3
    assert isinstance(messages[0], SystemMessage)
    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == user_msg
    mock_cprint.assert_called_with("💵 Cost: $ 0.1234\n", "green")


def test_agent_run_keyboard_interrupt():
    llm = MagicMock(spec=BaseChatModel)
    llm.return_value = AIMessage(content="Some response", additional_kwargs={})
    tool = MagicMock()
    tool.name = "test"
    tool.return_value = "Done"
    tools = [tool]
    agent = Agent(llm, tools)
    user_msg = "Run the agent with KeyboardInterrupt"
    with patch("codecraft.agent.cprint") as mock_cprint, patch("codecraft.agent.get_openai_callback") as mock_callback:
        mock_callback.return_value.__enter__.return_value.total_cost = 0.1234
        mock_callback.return_value.__enter__.return_value.total_cost = 0.1234
        with patch("codecraft.agent.yaspin"):
            with patch("codecraft.agent.Agent.next_step", side_effect=KeyboardInterrupt):
                try:
                    agent.run(user_msg)
                except KeyboardInterrupt:
                    mock_cprint.assert_called_with("💵 Cost: $ 0.1234\n", "green")
