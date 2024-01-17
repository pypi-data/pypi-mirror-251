import unittest
from unittest.mock import mock_open, patch

from codecraft.prompts import check_if_prompts_are_exists


class TestPrompts(unittest.TestCase):
    def test_check_if_prompts_are_exists(self):
        with patch("codecraft.prompts.os.path.exists") as mock_exists:
            mock_exists.side_effect = lambda *args, **kwargs: False
            with patch("codecraft.prompts.open", mock_open()) as mock_file:
                check_if_prompts_are_exists()
                mock_file.assert_any_call(".codecraft/prompts/SYSTEM_PROMPT.txt", "w")
                mock_file.assert_any_call(".codecraft/prompts/COVERAGE_INSTRUCTION.txt", "w")
                mock_exists.assert_any_call(".codecraft/prompts/SYSTEM_PROMPT.txt")
                mock_exists.assert_any_call(".codecraft/prompts/COVERAGE_INSTRUCTION.txt")
