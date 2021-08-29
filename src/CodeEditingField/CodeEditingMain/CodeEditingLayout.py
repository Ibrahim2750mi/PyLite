from PySide6 import QtWidgets, QtCore, QtGui
import builtins


def regex_converter(word_list: list) -> str:
    word_list = list(map(lambda word: [r"|\b" + word + r"\b" if word_list.index(word) != 0
                                       else r"\b" + word + r"\b"][0], word_list))

    return r''.join(word_list)


class CodeHighlightingField(QtGui.QSyntaxHighlighter):

    def __init__(self, editor: QtWidgets.QPlainTextEdit):
        super().__init__(editor.document())
        all_builtins = dir(builtins)
        python_builtins_functions = list(filter(lambda builtin: 'Error' not in builtin and
                                                                builtin.lower() == builtin, all_builtins))
        python_builtins_others = list(filter(lambda builtin: 'Error' not in builtin and
                                                             builtin.lower() != builtin, all_builtins))
        python_builtins_others += ['lambda', 'not', 'in', 'and', 'is', 'try', 'except', 'while', 'for', 'if',
                                   'elif', 'else', 'def', 'import', 'from', 'as', 'class']
        python_builtins_errors = list(filter(lambda builtin: 'Error' in builtin, all_builtins))
        self.time_in_sec = 0
        self.python_builtins_errors_regex = regex_converter(python_builtins_errors)
        self.python_builtins_functions_regex = regex_converter(python_builtins_functions)
        self.python_builtins_others_regex = regex_converter(python_builtins_others)

        self.string_formatting = QtGui.QTextCharFormat()
        self.string_formatting.setForeground(self.__format_color("62b543"))
        # --------------------------------------------
        self.function_formatting = QtGui.QTextCharFormat()
        self.function_formatting.setForeground(self.__format_color("bb9917"))
        # --------------------------------------------
        self.error_formatting = QtGui.QTextCharFormat()
        self.error_formatting.setForeground(self.__format_color("c75450"))
        # --------------------------------------------
        self.other_formatting = QtGui.QTextCharFormat()
        self.other_formatting.setForeground(self.__format_color('6897bb'))
        # --------------------------------------------
        self.decimal_formatting = QtGui.QTextCharFormat()
        self.decimal_formatting.setForeground(self.__format_color('40b6e0'))

    @staticmethod
    def __format_color(hex_string: str) -> QtGui.QBrush:
        r = hex_string[0:2]
        g = hex_string[2:4]
        b = hex_string[4:6]
        r = int(r[0], 16) * 16 + int(r[1], 16)
        g = int(g[0], 16) * 16 + int(g[1], 16)
        b = int(b[0], 16) * 16 + int(b[1], 16)

        x_color = QtGui.QColor(r, g, b)
        return x_color

    def __auto_regex_detection(self, x_expression: QtCore.QRegularExpressionMatchIterator,
                               x_formatter: QtGui.QTextCharFormat):
        match = x_expression.next()
        self.setFormat(match.capturedStart(), match.capturedLength(), x_formatter)

    def highlightBlock(self, text: str) -> None:

        string_expression = QtCore.QRegularExpression(r"(?<=\')[^\".]*?(?=\')|(?<=\")[^\'.]*?(?=\")")
        decimal_expression = QtCore.QRegularExpression(r'''\b[\d]+\b''')
        function_expression = QtCore.QRegularExpression(self.python_builtins_functions_regex)
        other_expression = QtCore.QRegularExpression(self.python_builtins_others_regex)
        error_expression = QtCore.QRegularExpression(self.python_builtins_errors_regex)

        # --------------------------------------------
        functions = function_expression.globalMatch(text)
        while functions.hasNext():
            self.__auto_regex_detection(functions, self.function_formatting)
        # --------------------------------------------
        errors = error_expression.globalMatch(text)
        while errors.hasNext():
            self.__auto_regex_detection(errors, self.error_formatting)
        # --------------------------------------------
        others = other_expression.globalMatch(text)
        while others.hasNext():
            self.__auto_regex_detection(others, self.other_formatting)
        # --------------------------------------------
        decimals = decimal_expression.globalMatch(text)
        while decimals.hasNext():
            self.__auto_regex_detection(decimals, self.decimal_formatting)
        # --------------------------------------------
        strings = string_expression.globalMatch(text)
        while strings.hasNext():
            self.__auto_regex_detection(strings, self.string_formatting)
