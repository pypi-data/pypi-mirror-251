from prompt_toolkit.completion import Completer, Completion


class AutoCompleter(Completer):
    def __init__(self, files, names, commands):
        self.commands = commands
        self.files = files
        self.names = names

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        words = text.split()
        if not words:
            return

        if text[0] == "/" and not (text[-1].isspace() or len(words) > 1):
            for cmd in self.commands:
                if cmd.startswith(text[1:]):
                    yield Completion(f"/{cmd}", start_position=-len(text), display=f"/{cmd}")
            return
        else:
            candidates = [(word, word) for word in self.files]
            if words[0] != "/add":
                candidates += [(word, f"`{word}`") for word in self.names]

        last_word = words[-1]
        for word_match, word_insert in candidates:
            if word_match.lower().startswith(last_word.lower()):
                yield Completion(word_insert, start_position=-len(last_word), display=word_match)
