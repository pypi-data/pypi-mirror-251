import os
import tempfile
from unittest.mock import patch

from langchain.schema import SystemMessage

from codecraft.context import context
from codecraft.core import run_session
from codecraft.prompts import SYSTEM_PROMPT

from ..agent import Agent
from ..core import apply_command, extract_cmd, get_prompt, is_command, load_files_content


def test_extract_cmd():
    assert extract_cmd("/add file.py") == ["add", "file.py"]
    assert extract_cmd("/prompt") == ("prompt", "")


def test_is_command():
    assert is_command("/add file.py") is True
    assert is_command("/prompt") is True
    assert is_command("not a command") is False


def test_load_files_content():
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf.write(b"Test content")
        tf.close()
        assert (
            load_files_content([tf.name])
            == f"""file {tf.name}:
```
Test content
```"""
        )
        os.unlink(tf.name)


def test_apply_command():
    with patch("codecraft.core.load_file_content", return_value=""):
        assert apply_command("/add test_file", []) == ["test_file"]
        assert apply_command("/prompt test_query", ["test_file"]) == ["test_file"]
    assert apply_command("/clear", ["test_file"]) == []


def test_get_prompt():
    assert get_prompt("Test instructions", [], show_repomap=False) == ""


def test_run_session_with_coverage():
    with patch("codecraft.core.ChatOpenAI") as mock_llm:
        mock_llm.return_value = None
        with patch("codecraft.core.Agent.run") as mock_agent_run:
            with patch("codecraft.core.get_coverage_prompt") as mock_get_coverage_prompt:
                mock_get_coverage_prompt.return_value = "coverage prompt"
                mock_agent_run.return_value = "coverage response"
                context.added_files = []
                response = run_session(coverage=True)
                mock_get_coverage_prompt.assert_called_once_with([])
                mock_agent_run.assert_called_once_with("coverage prompt")
                assert response == "coverage response"


@patch("codecraft.core.ChatOpenAI")
@patch("codecraft.core.prompt", return_value="/clear")
@patch("codecraft.core.apply_command", return_value=[])
@patch("codecraft.core.is_command", side_effect=[True, False])
@patch("codecraft.core.Agent.run")
@patch("codecraft.core.get_dev_prompt")
@patch("codecraft.core.get_repomap", return_value=("REPOSITORY STRUCTURE:\n...", []))
def test_run_session_interactive_prompt(
    mock_get_repomap,
    mock_get_dev_prompt,
    mock_agent_run,
    mock_is_command,
    mock_apply_command,
    mock_prompt,
    mock_chatopenai,
):
    """
    Test run_session function with interactive prompt.
    """
    mock_get_dev_prompt.return_value = "Mocked dev prompt"
    mock_agent_run.return_value = None

    response = run_session(coverage=False)

    mock_prompt.assert_called()
    mock_is_command.assert_called_with("/clear")
    mock_apply_command.assert_called_with("/clear", [])
    mock_get_dev_prompt.assert_called_with([], "/clear")
    mock_agent_run.assert_called_with("Mocked dev prompt")
    assert response is None


@patch("codecraft.core.ChatOpenAI")
@patch("codecraft.core.Agent.run")
@patch("codecraft.core.get_dev_prompt")
@patch("codecraft.core.get_repomap", return_value=("REPOSITORY STRUCTURE:\n...", []))
def test_run_session_with_query(mock_repomap, mock_get_dev_prompt, mock_agent_run, mock_chatopenai):
    """
    Test run_session function with a query parameter.
    """
    mock_get_dev_prompt.return_value = "Mocked dev prompt"
    mock_agent_run.return_value = "Mocked agent response"

    response = run_session(coverage=False, query="test query")

    mock_get_dev_prompt.assert_called_with([], "test query")
    mock_agent_run.assert_called_with("Mocked dev prompt")
    assert response == "Mocked agent response"


@patch("langchain.chat_models.ChatOpenAI")
def test_agent(mock_openai):
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k", streaming=True, verbose=True)
    tools = []

    agent = Agent(llm=llm, tools=tools)

    assert agent.messages == [SystemMessage(content=SYSTEM_PROMPT)]
    assert agent.tools == {}
    assert agent.functions == []
