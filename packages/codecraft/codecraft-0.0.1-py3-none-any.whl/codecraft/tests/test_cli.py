import argparse
from unittest.mock import MagicMock, patch

import codecraft.cli


def test_main_no_args():
    with patch("codecraft.cli.run_session") as mock_run_session:
        with patch(
            "argparse.ArgumentParser.parse_args",
            return_value=argparse.Namespace(coverage=False, query=None),
        ):
            codecraft.cli.main()
            mock_run_session.assert_called_once()


def test_main():
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(coverage=True, query=None),
    ):
        with patch("codecraft.cli.run_session") as mock_run_session:
            codecraft.cli.main()
            mock_run_session.assert_called_once_with(coverage=True)

    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(coverage=False, query=None),
    ):
        with patch("codecraft.cli.run_session") as mock_run:
            codecraft.cli.main()
            mock_run.assert_called_once_with()

    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(coverage=False, query="test query"),
    ):
        with patch("codecraft.cli.run_session") as mock_run_with_query:
            codecraft.cli.main()
            mock_run_with_query.assert_called_once_with(query="test query")
