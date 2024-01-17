import os
import subprocess

import requests
from langchain.tools import BaseTool


def git_push_to_remote():
    try:
        subprocess.check_output(["git", "push", "origin"])
        print("Changes pushed to remote origin successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def create_merge_request(
    source_branch,
    title,
    token=os.getenv("GITLAB_API_TOKEN"),
    project_id=os.getenv("GITLAB_PROJECT_ID"),
    target_branch=os.getenv("GITLAB_TARGET_BRANCH"),
) -> str:
    """
    Create a merge request on GitLab.

    Parameters:
    - token (str): Personal Access Token for GitLab.
    - project_id (int): ID of the project.
    - source_branch (str): Name of the source branch.
    - target_branch (str): Name of the target branch.
    - title (str): Title of the merge request.

    Returns:
    - dict: Response from GitLab API.
    """

    url = f"https://gitlab.welltory.com/api/v4/projects/{project_id}/merge_requests?access_token={token}"
    headers = {"Content-Type": "application/json"}
    data = {"source_branch": source_branch, "target_branch": target_branch, "title": title}

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        merge_request_data = response.json()
        return merge_request_data.get("web_url")
    else:
        response.raise_for_status()


class MergeRequestTool(BaseTool):
    name = "merge_request"
    description = (
        "Tool is useful to create merge request"
        "Format for the tool:"
        "- source_branch_name: name of the branch to merge to target branch"
        "- title: title for the merge request"
    )
    verbose = True

    def _run(self, source_branch_name: str, title: str) -> str:
        git_push_to_remote()
        mr_url = create_merge_request(
            source_branch=source_branch_name,
            title=title,
        )
        target_branch_name = os.getenv("GITLAB_TARGET_BRANCH")
        return (
            f"Merge request with title `{title}` created with source={source_branch_name} and target='{target_branch_name}'. "
            f"Its url is `{mr_url}`"
        )

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("_arun method is not implemented")
