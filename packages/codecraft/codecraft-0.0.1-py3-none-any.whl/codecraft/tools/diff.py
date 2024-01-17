import os
import subprocess

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field


def replace_string_in_file(filename, old_string, new_string):
    error = None
    # add check that file is exists
    if os.path.exists(filename):
        with open(filename, "r") as f:
            content = f.read()
        old_content = "".join(content)

        if old_string:
            if content.count(old_string) > 1:
                return f"Error: `original` is not unique in the file. File current content:\n```{content}```"

            content = content.replace(old_string, new_string, 1)
            if old_content == content:
                if old_string not in old_content and old_string != "":
                    return "Error: could not find `original` string in file"
                return "Error: updating failed - `original` and `updated` are the same"
        else:
            if old_content and not old_string:
                return "Error: Original parameter is empty but the file has content. Read file content first."
            content = new_string
        with open(filename, "w") as f:
            f.write(content)
            f.flush()
    else:
        with open(filename, "w") as f:
            f.write(new_string)
            f.flush()
    return error


def git_add_commit_all(filename, commit_message):
    try:
        subprocess.check_output(["git", "add", filename])
        subprocess.check_output(["git", "commit", "-m", f"CodeCraft: {commit_message}"])
        return "Files added and committed successfully."
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"


def diff(filename: str, original: str, updated: str, commit_message: str) -> str:
    errors = replace_string_in_file(filename, original, updated)
    if not errors:
        # git_add_commit_all(filename, commit_message)
        return f"File {filename} updated with commit message: {commit_message}"
    else:
        return errors


class DiffInput(BaseModel):
    filename: str = Field(description="File name to change")
    original: str = Field(
        description="Original code. To create new file it should be empty. It should be unique in the file"
    )
    updated: str = Field(description="New code")
    commit_message: str = Field(description="Message for GIT commit for provided changes")


diff_tool = StructuredTool.from_function(
    func=diff,
    name="diff",
    args_schema=DiffInput,
    description=(
        "Tool is useful for applying changes for local files. "
        "To create new file pass to the `original` parameter empty string."
        "To update existing file pass to `original` parameter part of the file to change."
        "Use compact form for JSON for function calling"
    ),
)


class GitCommitInput(BaseModel):
    filename: str = Field(description="File name to commit")
    commit_message: str = Field(description="Message for GIT commit for provided changes")


git_commit_tool = StructuredTool.from_function(
    func=git_add_commit_all,
    name="git_commit",
    args_schema=GitCommitInput,
    description=("Tool is useful for committing changes in GIT"),
)
