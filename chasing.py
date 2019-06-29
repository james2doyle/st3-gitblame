import sublime
import sublime_plugin


class BlameSetContentChasingMode(sublime_plugin.TextCommand):
    MODE_NONE = "<NONE>"
    MODE_SAME_FILE_SAME_COMMIT = "same_file_same_commit"
    MODE_CROSS_FILE_SAME_COMMIT = "cross_file_same_commit"
    MODE_CROSS_ANY_FILE = "cross_any_file"
    MODE_CROSS_ANY_HISTORICAL_FILE = "cross_any_historical_file"

    GIT_ARGS_FOR_MODES = {
        MODE_NONE: [],
        MODE_SAME_FILE_SAME_COMMIT: ["-M"],
        MODE_CROSS_FILE_SAME_COMMIT: ["-C"],
        MODE_CROSS_ANY_FILE: ["-C"] * 2,
        MODE_CROSS_ANY_HISTORICAL_FILE: ["-C"] * 3,
    }

    def run(self, edit, mode, permanence):
        if permanence:
            raise Exception("not implemented")
        else:
            self.view.settings().set(self.__class__.__name__, mode)

    def input(self, args):  # noqa: A003
        return ModeInputHandler()


class ModeInputHandler(sublime_plugin.ListInputHandler):
    def placeholder(self):
        return "Select a mode"

    def list_items(self):
        return [
            BlameSetContentChasingMode.MODE_NONE,
            BlameSetContentChasingMode.MODE_SAME_FILE_SAME_COMMIT,
            BlameSetContentChasingMode.MODE_CROSS_FILE_SAME_COMMIT,
            BlameSetContentChasingMode.MODE_CROSS_ANY_FILE,
            BlameSetContentChasingMode.MODE_CROSS_ANY_HISTORICAL_FILE,
        ]

    def next_input(self, args):
        return PermanenceInputHandler()

    def description(self, value, text):
        return 'to "{0}"'.format(text)


class PermanenceInputHandler(sublime_plugin.ListInputHandler):
    def list_items(self):
        return [
            ("Temporarily (for this open file)", False),
            ("Permanently (new default for all files)", True),
        ]
