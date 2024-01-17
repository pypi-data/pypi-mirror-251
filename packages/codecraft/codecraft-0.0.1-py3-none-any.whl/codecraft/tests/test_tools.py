import os
import subprocess
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch

from codecraft.tools.context import add_file_to_context, get_coverage_info
from codecraft.tools.git import (
    GitCheckoutBranchTool,
    GitNewBranchTool,
    checkout_branch,
    create_and_checkout_branch,
    get_current_branch,
)
from codecraft.tools.mr import git_push_to_remote
from codecraft.tools.pytest import run_test


class TestReplaceStringInFile(unittest.TestCase):
    def setUp(self):
        self.filename = "test_file.txt"
        self.old_string = "Hello, World!"
        self.new_string = "Hello, Python!"
        with open(self.filename, "w") as f:
            f.write(self.old_string)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)


def test_get_current_branch():
    with patch.object(subprocess, "run") as mock_run:
        mock_run.return_value.stdout = "main\n"
        mock_run.return_value.stdout = MagicMock()
        mock_run.return_value.stdout.strip = MagicMock(return_value="main")
    assert get_current_branch() == "main"


def test_checkout_branch():
    with patch.object(subprocess, "run") as mock_run:
        mock_run.return_value.stdout = MagicMock()
        mock_run.return_value.stdout.strip = MagicMock(return_value="main")
        mock_run.return_value.returncode = 0
        assert checkout_branch("main") == "Successfully switched to 'main'."


def test_create_and_checkout_branch():
    with patch.object(subprocess, "run") as mock_run:
        mock_run.return_value.stdout = "main\n"
        mock_run.return_value.stdout = MagicMock()
        mock_run.return_value.stdout.strip = MagicMock(return_value="main")
        mock_run.return_value.returncode = 0
        assert (
            create_and_checkout_branch("new_branch") == "Successfully created and switched to 'new_branch' from 'main'."
        )


def test_gitnewbranchtool():
    tool = GitNewBranchTool()
    with patch.object(subprocess, "run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "main\n"
        mock_run.return_value.stdout = MagicMock()
        mock_run.return_value.stdout.strip = MagicMock(return_value="main")
        assert tool._run("new_branch") == "Successfully created and switched to 'new_branch' from 'main'."


def test_gitcheckoutbranchtool():
    tool = GitCheckoutBranchTool()
    with patch.object(subprocess, "run") as mock_run:
        mock_run.return_value.returncode = 0
        assert tool._run("main") == "Successfully switched to 'main'."


def test_git_new_branch_tool_error():
    with patch.object(subprocess, "run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "error message"
        tool = GitNewBranchTool()
        response = tool.run("test_branch")
        assert response == "Error: error message"


def test_git_checkout_branch_tool_error():
    with patch.object(subprocess, "run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "error message"
        tool = GitCheckoutBranchTool()
        response = tool.run("test_branch")
        assert response == "Error: error message"


def test_get_coverage_info():
    result = get_coverage_info("codecraft/tools/pytest.py")
    assert "executed" in result
    assert "missing (not executed)" in result
    assert "excluded" in result


def test_run_test_coverage_report():
    # Test that the coverage report command is executed
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="Test Passed", stderr=None)
        output = run_test("path/to/test")
        mock_run.assert_called_with(
            ["coverage", "report", "--sort=-cover"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        assert "Test Passed" in output

    assert run_test("codecraft/tests/test_agent.py") is not None


@patch("subprocess.check_output")
def test_git_push_to_remote_success(mock_check_output):
    # Arrange
    mock_check_output.return_value = b""

    # Act
    git_push_to_remote()

    # Assert
    mock_check_output.assert_called_once_with(["git", "push", "origin"])


@patch("subprocess.check_output")
def test_git_push_to_remote_failure(mock_check_output):
    # Arrange
    mock_check_output.side_effect = subprocess.CalledProcessError(1, "cmd")

    # Act
    git_push_to_remote()

    # Assert
    mock_check_output.assert_called_once_with(["git", "push", "origin"])


def test_get_coverage_info_error():
    """
    Test get_coverage_info function when coverage info retrieval fails.
    """
    # Setup
    filename = "non_existent_file.py"
    with_coverage = True

    # Mock subprocess.run to simulate coverage annotate command failure
    with mock.patch("codecraft.tools.context.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "No such file or directory"
        # Execute
        result = get_coverage_info(filename)
        assert result is not None

        # Assert
        assert "No such file or directory" in result

def test_run_test_failure():
    """
    Test run_test function when the test run fails.
    """
    # Setup
    path = "path/to/failing_test"
    expected_output = "Test failed\n\nSome error message"

    # Mock subprocess.run to simulate a failing test run
    with mock.patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "Test failed"
        mock_run.return_value.stderr = "Some error message"

        # Execute
        result = run_test(path)

        # Assert
        assert result == expected_output

    """
    Test get_coverage_info function when coverage info retrieval fails.
    """
    # Setup
    filename = "non_existent_file.py"
    with_coverage = True

    # Mock subprocess.run to simulate coverage annotate command failure
    with mock.patch("codecraft.tools.context.subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "No such file or directory"
        # Execute
        result = get_coverage_info(filename)
        assert result is not None

        # Assert
        assert "No such file or directory" in result


import os
import pytest
from unittest.mock import mock_open, patch
from codecraft.tools.context import add_file_to_context, get_coverage_info


def test_add_file_to_context_with_coverage():
    test_filename = 'test_file.py'
    test_coverage_data = '> def test_function():\n>     pass\n! missing_line = None'
    m = mock_open(read_data=test_coverage_data)
    with patch('builtins.open', m):
        with patch('os.path.exists', return_value=True):
            with patch('subprocess.run') as mock_run:
                mock_run.return_value.returncode = 0
                result = add_file_to_context(test_filename, with_coverage=True)
                assert 'missing_line = None' in result
                assert result.startswith('\n> executed\n! missing (not executed)\n- excluded\n\n')


    """
    Test add_file_to_context function when coverage info retrieval fails.
    """
    # Setup
    filename = "non_existent_file.py"
    with_coverage = True

    # Execute
    result = add_file_to_context(filename, with_coverage)

    # Assert
    assert "Error: file non_existent_file.py does not exist" in result


def test_add_file_to_context_without_coverage():
    # Prepare
    filename = "codecraft/tools/context.py"
    expected_result = "Added codecraft/tools/context.py to the context."
    # Execute
    result = add_file_to_context(filename)
    # Assert
    assert expected_result in result

    # Test with non-existing file
    filename = "non_existing_file.py"
    expected_result = "Error: file non_existing_file.py does not exist"
    result = add_file_to_context(filename)
    assert result == expected_result
