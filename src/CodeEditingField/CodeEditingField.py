from PySide6 import QtWidgets, QtGui, QtCore
import builtins
from copy import deepcopy
import re
import time as te


class CodeEditingField(QtWidgets.QTextEdit):
    COLOR_FORMAT = ["<span style=\"color:", "", ";\">", "", "</span>"]
    WORD_REGEX = re.compile(
        r'''"[^"]*"|'[^']*'|\b([^\d\W]+)\b'''
    )
    NUMBER_REGEX = re.compile(
        r"\b[\d]+\b"
    )

    # (?<![\S"])([^"\s]+)(?![\S"])|(?<![\S'])([^'\s]+)(?![\S'])
    STRING_REGEX = re.compile(
        r"\'[^\".]*?\'|\"[^\'.]*?\""
    )
    PYTHON_BUILTINS_FUNCTIONS_COLOR = deepcopy(COLOR_FORMAT)
    PYTHON_BUILTINS_FUNCTIONS_COLOR[1] = "#bb9917"
    NORMAL_TEXT = deepcopy(COLOR_FORMAT)
    NORMAL_TEXT[1] = "#000000"
    PYTHON_BUILTINS_ERRORS_COLOR = deepcopy(COLOR_FORMAT)
    PYTHON_BUILTINS_ERRORS_COLOR[1] = "#c75450"
    PYTHON_BUILTINS_OTHERS_COLOR = deepcopy(COLOR_FORMAT)
    PYTHON_BUILTINS_OTHERS_COLOR[1] = "#6897bb"
    PYTHON_DECIMALS_COLOR = deepcopy(COLOR_FORMAT)
    PYTHON_DECIMALS_COLOR[1] = "#40b6e0"
    PYTHON_STRING_COLOR = deepcopy(COLOR_FORMAT)
    PYTHON_STRING_COLOR[1] = "#62b543"

    Green = QtGui.QColor(98, 181, 67)

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
        self.string = []
        self.recursion = 0
        self.time = te.perf_counter()
        self.just_changed = False

    @QtCore.Slot()
    def current_text(self) -> None:
        position_words = 0
        position_number = 0
        position_string = 0
        text = self.toPlainText()
        res_words = self.WORD_REGEX.search(text[position_words:])
        res_numbers = self.NUMBER_REGEX.search(text[position_number:])
        res_strings = self.STRING_REGEX.search(text[position_number:])
        while res_words:
            position_words, res_words = self.auto(position=position_words, res=res_words)
        while res_numbers:
            position_number, res_numbers = self.auto(position_number, res_numbers)
        while res_strings:
            position_string, res_strings = self.auto(position_string, res_strings, 1)

    def change_size(self, mw: int, mh: int, max_: bool = True) -> None:
        if max_:
            self.setMaximumSize(mw, mh)
        else:
            self.setMinimumSize(mw, mh)

        return None

    def __replace_word(self, start, word, new_word, n_factor):
        if te.perf_counter() - self.time > 0.01:
            if word not in self.string and self.__condition(word, n_factor):
                cursor = QtGui.QTextCursor(self.document())
                cursor.setPosition(start)
                if word[0] == "\"" and word[-1] == "\"" and len(word)> n_factor:
                    length = len(word) - n_factor
                    worker = True
                elif word[0] == "\'" and word[-1] == "\'" and len(word)> n_factor:
                    length = len(word) - n_factor
                    worker = True
                else:
                    length = len(word)
                    move = QtGui.QTextCursor.MoveOperation.Right
                    worker = False

                cursor.movePosition(
                    QtGui.QTextCursor.MoveOperation.Right,
                    QtGui.QTextCursor.MoveMode.KeepAnchor,
                    length,
                )
                self.string.append(word)
                self.__regulator()
                cursor.deleteChar()
                if worker:
                    cursor.deleteChar()
                self.time = te.perf_counter()
                cursor.insertHtml(new_word)
                if worker:
                    cursor.setPosition(cursor.position()-1)
                    self.setTextCursor(cursor)
        else:
            self.time = te.perf_counter()
            


    def __check(self, word) -> str:
        format_ = None
        if word in dir(builtins):
            if word in self.python_builtins_functions:
                format_ = deepcopy(self.PYTHON_BUILTINS_FUNCTIONS_COLOR)
            elif word in self.python_builtins_errors:
                format_ = deepcopy(self.PYTHON_BUILTINS_ERRORS_COLOR)
            elif word in self.python_builtins_others:
                format_ = deepcopy(self.PYTHON_BUILTINS_OTHERS_COLOR)
        elif word[0] in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0"):
            format_ = deepcopy(self.PYTHON_DECIMALS_COLOR)
        elif word[0] == "\"" and word[-1] == "\"":
            format_ = deepcopy(self.PYTHON_STRING_COLOR)
        elif word[0] == "\'" and word[-1] == "\'":
            format_ = deepcopy(self.PYTHON_STRING_COLOR)
        else:
            format_ = deepcopy(self.NORMAL_TEXT)
        format_[3] = word
        return ''.join(format_)

    def auto(self, position, res, n_factor=0):
        word = res.group()
        self.recursion = 1
        correct_word = self.__check(word)
        position += res.start()
        if n_factor == 1: 
            if word[0] == "\"" and word[-1] == "\"":
                if correct_word:
                    self.__replace_word(position, word, correct_word, n_factor)
                    position += len(word)
                else:
                    position += len(word)
                text = self.toPlainText()
                return position, self.WORD_REGEX.search(text[position:])  
            elif word[0] == "\'" and word[-1] == "\'":
                if correct_word:
                    self.__replace_word(position, word, correct_word, n_factor)
                    position += len(word)
                else:
                    position += len(word)
                text = self.toPlainText()
                return position, self.WORD_REGEX.search(text[position:])
            else:
                position += len(word)
                text = self.toPlainText()
                return position, self.WORD_REGEX.search(text[position:])

        else:
            if correct_word:
                self.__replace_word(position, word, correct_word, n_factor)
                position += len(word)
            else:
                position += len(word)
            text = self.toPlainText()
            return position, self.WORD_REGEX.search(text[position:])

    @staticmethod
    def __condition(word, n_factor):
        if n_factor == 1:
            if '"' in word or "'" in word:
                return True
            else:
                return False
        else:
            return True

    def __regulator(self):
        self.string = list(filter(lambda elem: "'" in elem or '"' in elem, self.string))
