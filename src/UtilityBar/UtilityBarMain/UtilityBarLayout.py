import ast
import builtins

from PySide6 import QtWidgets


class UtilityDocker(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super(UtilityDocker, self).__init__()

    def change_size(self, mw: int, mh: int) -> None:
        self.setFixedSize(mw, mh)
        return None

    def change_line_wrap(self) -> None:
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)


# noinspection PyBroadException
class UtilityButtons(QtWidgets.QPushButton):
    def __init__(self, num: int, docker: UtilityDocker, text: str = ""):
        # Accepting UtilityDocker as argument to change the text within it.
        super(UtilityButtons, self).__init__(text=text)
        self.docker = docker
        if num == 1:
            self.clicked.connect(self.variable_function)
            self.variables = []
            self.all_builtins = dir(builtins) + ['lambda', 'not', 'in', 'and', 'is', 'try', 'except', 'while', 'for',
                                                 'if',
                                                 'elif', 'else', 'def', 'import', 'from', 'as', 'class']
        elif num == 2:
            self.clicked.connect(self.gen_info_function)

        elif num == 3:
            self.clicked.connect(self.documentation_function)

    def variable_function(self, text):
        try:
            st = ast.parse(text)
        except Exception as _:
            pass
        else:
            self.variables = ["Variables:"]
            for node in ast.walk(st):
                if type(node) is ast.Name and node.id not in self.variables and node.id not in self.all_builtins:
                    self.variables.append(node.id)

        self.docker.setPlainText('\n'.join(self.variables))

    def gen_info_function(self, text):
        gen_info_text = f"General Information:\n\n"
        error_text = ""
        try:
            ast.parse(text)
        except Exception as e:
            if e.args != ('compile() arg 1 must be a string, bytes or AST object',):
                error_text = f"Errors:\n{e.args[0]} at line number:" \
                                          f"{e.args[1][1]} column number:{e.args[1][2]}"
        self.docker.setPlainText(gen_info_text+error_text)

    def documentation_function(self):
        pass
