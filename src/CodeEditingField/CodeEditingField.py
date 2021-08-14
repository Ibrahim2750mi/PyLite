from PySide6 import QtWidgets, QtGui
import builtins
from copy import deepcopy
import re


class CodeEditingField(QtWidgets.QTextEdit):
    COLOR_FORMAT = ["<span style=\"color:", "", ";\">", "", "</span>"]
    WORD_REGEX = re.compile(
        r"\b[^\d\W]+\b"
    )
    PYTHON_BUILTINS_FUNCTIONS_COLOR = deepcopy(COLOR_FORMAT)
    PYTHON_BUILTINS_FUNCTIONS_COLOR[1] = "#bb9917"
    NORMAL_TEXT = deepcopy(COLOR_FORMAT)
    NORMAL_TEXT[1] = "#000000"
    PYTHON_BUILTINS_ERRORS_COLOR = deepcopy(COLOR_FORMAT)
    PYTHON_BUILTINS_ERRORS_COLOR[1] = "#c75450"
    PYTHON_BUILTINS_OTHERS_COLOR = deepcopy(COLOR_FORMAT)
    PYTHON_BUILTINS_OTHERS_COLOR[1] = "#6897bb"

    BLACK = QtGui.QColor(0, 0, 0)

    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.current_text)
        all_builtins = dir(builtins)
        self.last_word = ""
        self.python_builtins_functions = list(filter(lambda builtin: 'Error' not in builtin and
                                                                     builtin.lower() == builtin, all_builtins))
        self.python_builtins_others = list(filter(lambda builtin: 'Error' not in builtin and
                                                                  builtin.lower() != builtin, all_builtins))
        self.python_builtins_errors = list(filter(lambda builtin: 'Error' in builtin, all_builtins))

        # self.PYTHON_BUILTINS_FUNCTIONS_COLOR = deepcopy(self.COLOR_FORMAT)
        # self.PYTHON_BUILTINS_FUNCTIONS_COLOR[1] = "#bb9917"
        self.cached_text = []
        self.whole_cache = ""
        self.recursion = 0
        self.just_changed = False

    def current_text(self) -> None:
        if self.just_changed:
            self.just_changed = False
        else:
            if self.recursion != 0:
                self.recursion = 0
                self.just_changed = True
            else:
                position = 0
                text = self.toPlainText()
                res = self.WORD_REGEX.search(text[position:])
                while res:
                    word = res.group()
                    self.recursion = 1
                    correct_word = self.__check(word)
                    position += res.start()
                    if correct_word:
                        self.__replace_word(position, word, correct_word)
                        position += len(word)
                    else:
                        position += len(word)
                    text = self.toPlainText()
                    res = self.WORD_REGEX.search(text[position:])

    def change_size(self, mw: int, mh: int, max_: bool = True) -> None:
        if max_:
            self.setMaximumSize(mw, mh)
        else:
            self.setMinimumSize(mw, mh)

        return None

    def __replace_word(self, start, word, new_word):
        cursor = QtGui.QTextCursor(self.document())
        cursor.setPosition(start)
        cursor.movePosition(
            QtGui.QTextCursor.MoveOperation.Right,
            QtGui.QTextCursor.MoveMode.KeepAnchor,
            len(word),
        )
        cursor.deleteChar()
        cursor.insertHtml(new_word)
        self.just_changed = True

    def __check(self, word) -> str:
        format_ = None
        if word in dir(builtins):
            if word in self.python_builtins_functions:
                format_ = deepcopy(self.PYTHON_BUILTINS_FUNCTIONS_COLOR)
            elif word in self.python_builtins_errors:
                format_ = deepcopy(self.PYTHON_BUILTINS_ERRORS_COLOR)
            elif word in self.python_builtins_others:
                format_ = deepcopy(self.PYTHON_BUILTINS_OTHERS_COLOR)
        else:
            format_ = deepcopy(self.NORMAL_TEXT)
        format_[3] = word
        return ''.join(format_)
