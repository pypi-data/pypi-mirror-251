import unittest
from unittest.mock import Mock

from prompt_toolkit.completion import Completion

from ..completer import AutoCompleter


class TestAutoCompleter(unittest.TestCase):
    def setUp(self):
        self.files = ["file1", "file2"]
        self.names = ["name1", "name2"]
        self.commands = ["command1", "command2"]
        self.completer = AutoCompleter(self.files, self.names, self.commands)

    def test_init(self):
        self.assertEqual(self.completer.files, self.files)
        self.assertEqual(self.completer.names, self.names)
        self.assertEqual(self.completer.commands, self.commands)

    def test_get_completions(self):
        # Test when text is empty
        document = Mock()
        document.text_before_cursor = ""
        completions = list(self.completer.get_completions(document, None))
        self.assertEqual(completions, [])

        # Test when text starts with '/'
        document.text_before_cursor = "/com"
        completions = list(self.completer.get_completions(document, None))
        self.assertEqual(completions, [Completion("/command1", -4, "/command1"), Completion("/command2", -4, "/command2")])

        # Test when text does not start with '/'
        document.text_before_cursor = "fi"
        completions = list(self.completer.get_completions(document, None))
        self.assertEqual(completions, [Completion("file1", -2, "file1"), Completion("file2", -2, "file2")])
