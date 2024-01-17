import subprocess

from langchain.tools import BaseTool


def get_current_branch():
    """
    Get the name of the current branch in the local git repository.

    Returns:
    - str: The name of the current branch, or None if an error occurred.
    """
    result = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()
    else:
        return None


def checkout_branch(branch_name):
    result = subprocess.run(["git", "checkout", branch_name], capture_output=True, text=True)
    if result.returncode == 0:
        return f"Successfully switched to '{branch_name}'."
    else:
        return f"Error: {result.stderr}"


def create_and_checkout_branch(branch_name):
    """
    Create and checkout to a new branch in local git

    Args:
    - branch_name (str): The name of the branch without the prefix.

    Returns:
    - str: A message indicating success or failure.
    """

    current_branch_name = get_current_branch()

    # Create and checkout the new branch
    result = subprocess.run(["git", "checkout", "-b", branch_name], capture_output=True, text=True)

    if result.returncode == 0:
        return f"Successfully created and switched to '{branch_name}' from '{current_branch_name}'."
    else:
        result = subprocess.run(["git", "checkout", branch_name], capture_output=True, text=True)
        if result.returncode == 0:
            return f"Successfully created and switched to '{branch_name}' from '{current_branch_name}'."
        else:
            return f"Error: {result.stderr}"


class GitNewBranchTool(BaseTool):
    name = "git_new_branch"
    description = (
        "Tool is useful to create and checkout new branch in local git."
        "Format for this tool: "
        "branch_name: name of the new branch"
    )
    verbose = True

    def _run(self, branch_name: str) -> str:
        response = create_and_checkout_branch(branch_name)
        return response


class GitCheckoutBranchTool(BaseTool):
    name = "git_checkout_branch"
    description = (
        "Tool is useful to checkout a branch in local git."
        "Format for this tool: "
        "branch_name: name of the branch to checkout"
    )
    verbose = True

    def _run(self, branch_name: str) -> str:
        response = checkout_branch(branch_name)
        return response
