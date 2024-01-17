from unittest.mock import patch

import pytest
import requests

from codecraft.tools.mr import MergeRequestTool, create_merge_request


def test_create_merge_request_success():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {"web_url": "mock_url"}
        result = create_merge_request("source_branch", "title")
        assert result == "mock_url"


def test_create_merge_request_failure():
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 400
        mock_post.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
        with pytest.raises(requests.exceptions.HTTPError):
            create_merge_request("source_branch", "title")


def test_merge_request_tool_run():
    with patch("codecraft.tools.mr.create_merge_request") as mock_create_merge_request, patch(
        "os.getenv"
    ) as mock_getenv:
        mock_create_merge_request.return_value = "mock_url"
        mock_getenv.return_value = "target_branch"
        tool = MergeRequestTool()
        result = tool._run("source_branch", "title")
        assert (
            result
            == "Merge request with title `title` created with source=source_branch and target='target_branch'. Its url is `mock_url`"
        )


import asyncio


def test_merge_request_tool_arun():
    tool = MergeRequestTool()
    with pytest.raises(NotImplementedError):
        asyncio.run(tool._arun("query"))
