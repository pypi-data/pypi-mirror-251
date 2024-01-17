import os
import subprocess
import unittest
from unittest.mock import patch

from codecraft.tools.diff import diff, git_add_commit_all, replace_string_in_file


class TestDiff(unittest.TestCase):
    def test_replace_string_in_file_error_unique(self):
        """
        Test replace_string_in_file when 'original' is not unique in the file.
        """
        filename = "test_file.py"
        original = "duplicate_line"
        updated = "new_content"
        with open(filename, "w") as f:
            f.write("duplicate_line\nduplicate_line\n")
        result = replace_string_in_file(filename, original, updated)
        assert result == (
            "Error: `original` is not unique in the file. File current content:\n"
            "```duplicate_line\n"
            "duplicate_line\n"
            "```"
        )
        os.remove(filename)

    def test_replace_string_in_file_file_not_exist(self):
        """
        Test replace_string_in_file when the file does not exist.
        """
        filename = "nonexistent_test_file.txt"
        if os.path.exists(filename):
            os.remove(filename)
        original = ""
        updated = "Hello, Python!"
        result = replace_string_in_file(filename, original, updated)
        self.assertIsNone(result)
        with open(filename, "r") as f:
            content = f.read()
            self.assertEqual(content, updated)
        os.remove(filename)

    def test_replace_string_in_file_empty_original_new_file(self):
        """
        Test replace_string_in_file when 'original' is empty and creating a new file.
        """
        filename = "empty_original_new_file_test.txt"
        original = ""
        updated = "Content for new file"
        with open(filename, "w") as f:
            f.write(original)
        result = replace_string_in_file(filename, original, updated)
        self.assertIsNone(result)
        with open(filename, "r") as f:
            content = f.read()
            self.assertEqual(content, updated)
        os.remove(filename)


def test_replace_string_in_file():
    filename = "test_file.txt"
    original = "Hello, World!"
    updated = "Hello, Python!"
    with open(filename, "w") as f:
        f.write(original)
    replace_string_in_file(filename, original, updated)
    with open(filename, "r") as f:
        assert f.read() == updated
    os.remove(filename)


def test_diff():
    filename = "test_file.txt"
    original = "Hello, World!"
    updated = "Hello, Python!"
    commit_message = "Update greeting"
    with patch("codecraft.tools.diff.replace_string_in_file", return_value=None):
        with patch("codecraft.tools.diff.git_add_commit_all", return_value=None):
            result = diff(filename, original, updated, commit_message)
            assert result == f"File {filename} updated with commit message: {commit_message}"


def test_diff_errors():
    """
    Test the diff function for error handling.
    """
    # Mock the replace_string_in_file to return an error message
    with patch(
        "codecraft.tools.diff.replace_string_in_file",
        return_value="Error: updating failed - `original` and `updated` are the same",
    ):
        result = diff("dummy_file.py", "original content", "original content", "Test commit message")
        assert result == "Error: updating failed - `original` and `updated` are the same"

    with patch(
        "codecraft.tools.diff.replace_string_in_file", return_value="Error: could not find `original` string in file"
    ):
        result = diff("dummy_file.py", "nonexistent content", "updated content", "Test commit message")
        assert result == "Error: could not find `original` string in file"


def test_replace_string_in_file_no_original_with_content():
    # Setup: create a temporary file with content
    with open("temp_file.txt", "w") as f:
        f.write("Existing content")

    # Test: Call replace_string_in_file with no original string but the file has content
    error_message = replace_string_in_file("temp_file.txt", "", "New content")

    # Verify: The error message should indicate that the original parameter is empty but the file has content
    assert error_message == "Error: Original parameter is empty but the file has content. Read file content first."

    # Cleanup: remove the temporary file
    os.remove("temp_file.txt")

    """
    Test the diff function for error handling.
    """
    # Mock the replace_string_in_file to return an error message
    with patch(
        "codecraft.tools.diff.replace_string_in_file",
        return_value="Error: updating failed - `original` and `updated` are the same",
    ):
        result = diff("dummy_file.py", "original content", "original content", "Test commit message")
        assert result == "Error: updating failed - `original` and `updated` are the same"

    with patch(
        "codecraft.tools.diff.replace_string_in_file", return_value="Error: could not find `original` string in file"
    ):
        result = diff("dummy_file.py", "nonexistent content", "updated content", "Test commit message")
        assert result == "Error: could not find `original` string in file"


def test_replace_string_in_file_same_original_updated():
    filename = "test_file.txt"
    original = "This is a test string."
    updated = original
    with open(filename, "w") as f:
        f.write(original)
    error = replace_string_in_file(filename, original, updated)
    assert error == "Error: updating failed - `original` and `updated` are the same"
    os.remove(filename)

    # Test error when 'original' string is not found

    def test_replace_string_in_file_create_new_file(self):
        """
        Test replace_string_in_file when creating a new file with new content.
        """
        filename = "new_test_file.txt"
        original = ""
        updated = "New file content"
        result = replace_string_in_file(filename, original, updated)
        self.assertIsNone(result)
        with open(filename, "r") as f:
            content = f.read()
            self.assertEqual(content, updated)
        os.remove(filename)

    filename = "test_file.txt"
    with open(filename, "w") as f:
        f.write("This is a test file.")
    error = replace_string_in_file(filename, "nonexistent", "new")
    assert error == "Error: could not find `original` string in file"


def test_replace_string_in_file_error_handling():
    """
    Test the diff function for error handling.
    """
    # Mock the replace_string_in_file to return an error message
    with patch(
        "codecraft.tools.diff.replace_string_in_file",
        return_value="Error: updating failed - `original` and `updated` are the same",
    ):
        result = diff("dummy_file.py", "original content", "original content", "Test commit message")
        assert result == "Error: updating failed - `original` and `updated` are the same"

    with patch(
        "codecraft.tools.diff.replace_string_in_file", return_value="Error: could not find `original` string in file"
    ):
        result = diff("dummy_file.py", "nonexistent content", "updated content", "Test commit message")
        assert result == "Error: could not find `original` string in file"

    # Add the new test after existing tests
    # Test to cover error handling in git_add_commit_all function
    with patch("subprocess.check_output", side_effect=subprocess.CalledProcessError(1, ["git"])):
        result = git_add_commit_all("nonexistent_file.txt", "Test commit message")
        assert "An error occurred" in result

    filename = "test_file.txt"
    commit_message = "Update greeting"
    with patch("subprocess.check_output", return_value=None):
        git_add_commit_all(filename, commit_message)
