from PySide6 import QtWidgets, QtGui
import builtins
from copy import deepcopy
import re


class CodeEditingField(QtWidgets.QTextEdit):
    COLOR_FORMAT = ["<span style=\"color:", "", ";\">", "", "</span>"]
    WORD_REGEX = r"\b[^\d\W\?]+\b"
    PYTHON_BUILTINS_FUNCTIONS_COLOR = deepcopy(COLOR_FORMAT)
    PYTHON_BUILTINS_FUNCTIONS_COLOR[1] = "#bb9917"
    NORMAL_TEXT = deepcopy(COLOR_FORMAT)
    NORMAL_TEXT[1] = "#000000"
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
        if not self.just_changed:
            text = self.toPlainText()
            if len(text) > len(self.whole_cache):
                new_text = text.replace("\n", " ")
                res = new_text.split(" ")
                if self.recursion != 0:
                    self.just_changed = True
                    self.recursion = 0
                else:
                    print(res, self.cached_text)
                    edited_text = list(set(res) - set(self.cached_text))
                    edited_text = list(filter(lambda word: word != "", edited_text))
                    position_hint = self.textCursor().position()
                    if len(edited_text) > 0:
                        last_word = edited_text[0]
                        if last_word in dir(builtins):
                            actual_pos = self.__riv(last_word, position_hint, text)
                            print("not a whole word", last_word)
                            self.just_changed = True
                            self.recursion = 1
                            if last_word in self.python_builtins_functions:

                                new_last_word = deepcopy(self.PYTHON_BUILTINS_FUNCTIONS_COLOR)
                                new_last_word[3] = last_word
                                new_last_word = ''.join(new_last_word)
                                self.__replace_word(actual_pos, last_word, new_last_word)
                    else:
                        last_word = self.cached_text[-1]
                        actual_pos = position_hint - len(last_word) - 1
                        print("a whole word", last_word)
                        self.just_changed = True
                        self.recursion = 1
                        new_last_word = deepcopy(self.NORMAL_TEXT)
                        new_last_word[3] = last_word
                        new_last_word = ''.join(new_last_word)
                        print(new_last_word)
                        self.__replace_word(actual_pos, last_word, new_last_word)
            
                self.cached_text = res
            self.whole_cache = text
        else:
            self.just_changed = False

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

    @staticmethod
    def __riv(last_word, position_hint, text):
        for inc_x in range(0, len(last_word) + 1):

            if last_word == text[position_hint + inc_x: position_hint + len(last_word) + inc_x]:
                position_hint = position_hint + inc_x
                break
            elif last_word == text[position_hint - inc_x: position_hint + len(last_word) - inc_x]:
                position_hint = position_hint - inc_x
                break
        return position_hint
