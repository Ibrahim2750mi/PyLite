from PySide6 import QtWidgets, QtCore

import os
import sys

sys.path.append(os.path.realpath('.'))

from TaskBar.TaskBarLayout import TaskBarContent
from UtilityBar.UtilityBarLayout import UtilityButtons


class CodeEditingField(QtWidgets.QPlainTextEdit):
    def __init__(self, line_labeler: TaskBarContent, variable_button: UtilityButtons, error_button: UtilityButtons):
        super().__init__()
        self.textChanged.connect(self.on_text_change)
        self.variables = []
        self.label_line = line_labeler
        self.variable_button = variable_button
        self.error_button = error_button
        self.previous_postion = 0

    @QtCore.Slot()
    def on_text_change(self):
        # try:
        #     st = ast.parse(self.toPlainText())
        # except Exception as e:
        #     pass
        # else:
        #     self.variables = []
        #     for node in ast.walk(st):
        #         if type(node) is ast.Name:
        #             self.variables.append(node.id)
        self.variable_button.variable_function(self.toPlainText())
        self.error_button.error_function(self.toPlainText())
        self.previous_postion = self.textCursor().position()
        self.label_line.line_and_column_number(self.toPlainText(), self.textCursor().position())

    def change_size(self, mw: int, mh: int, max_: bool = True) -> None:
        if max_:
            self.setMaximumSize(mw, mh)
        else:
            self.setMinimumSize(mw, mh)

        return None

    def change_line_wrap(self) -> None:
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)




    # def set_co_ordinate(self, x: int, y: int):
    #     self.setStyleSheet(f'padding-left: {x}px; padding-top: {y}px;')

