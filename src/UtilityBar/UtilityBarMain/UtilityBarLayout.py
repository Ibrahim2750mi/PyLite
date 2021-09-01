from .UtilityAstAnalyzer import Analyzer

import ast
import builtins

import autopep8
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
            self.analyzer = Analyzer()

        elif num == 2:
            self.clicked.connect(self.gen_info_function)

        elif num == 3:
            self.clicked.connect(self.documentation_function)

    def variable_function(self, text):
        try:
            tree = ast.parse(text)
        except Exception as _:
            pass
        else:
            self.analyzer = Analyzer()
            self.analyzer.visit(tree)
            code_data = self.analyzer.report()
            docker_text = ""
            try:
                for k, vs in code_data.items():
                    docker_text += f"{k[0].upper()+k[1:]}:\n"
                    for v in vs:
                        docker_text += f"{v}\n"
                    docker_text += "\n"
            except ValueError:
                pass
            else:
                self.docker.setPlainText(docker_text)

    def gen_info_function(self, text):
        gen_info_text = f"General Information:\n\n"
        error_text = ""
        fix_text = ""
        try:
            ast.parse(text)
        except Exception as e:
            if e.args != ('compile() arg 1 must be a string, bytes or AST object',):
                error_text = f"Errors:\n{e.args[0]} at line number:" \
                             f"{e.args[1][1]} column number:{e.args[1][2]}\n\n"
                if e.args[0] == "unexpected EOF while parsing":
                    if autopep8.count_unbalanced_brackets(text) > 0:
                        fix_text = "Fix:\nTry adding a closing-parenthesis(')', ']', '}') to fix this error"
                    else:
                        fix_text = "Fix:\nNo fix found :("

        self.docker.setPlainText(gen_info_text + error_text + fix_text)

    def documentation_function(self):
        pass
