import unittest
from unittest.mock import patch

from codecraft.tools.git import create_and_checkout_branch


class TestGitTools(unittest.TestCase):
    @patch("codecraft.tools.git.subprocess.run")
    def test_create_and_checkout_branch_existing_branch(self, mock_run):
        mock_run.side_effect = [
            unittest.mock.MagicMock(returncode=0),  # Simulate branch creation failure
            unittest.mock.MagicMock(returncode=1),  # Simulate successful checkout
            unittest.mock.MagicMock(returncode=0),  # Simulate successful checkout
        ]
        result = create_and_checkout_branch("existing_branch")
        self.assertIn("Successfully created and switched to 'existing_branch'", result)
        assert mock_run.call_count == 3
