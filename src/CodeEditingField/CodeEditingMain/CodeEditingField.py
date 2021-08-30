import os
import pickle
import sys

from PySide6 import QtWidgets, QtCore

sys.path.append(os.path.realpath('.'))

from TaskBar.TaskBarMain.TaskBarLayout import TaskBarContent
from UtilityBar.UtilityBarMain.UtilityBarLayout import UtilityButtons


class CodeEditingField(QtWidgets.QPlainTextEdit):
    def __init__(self, line_labeler: TaskBarContent, variable_button: UtilityButtons, error_button: UtilityButtons):
        super().__init__()
        self.textChanged.connect(self.on_text_change)
        self.cursorPositionChanged.connect(self.on_cursor_change)
        self.label_line = line_labeler
        self.variable_button = variable_button
        self.error_button = error_button

        with open("../assets/assets.pickle", "rb") as f:
            colors = pickle.load(f)
            bg = colors["background"]
        self.setStyleSheet("QPlainTextEdit {" + f"background-color: #{bg};" + "}")
        self.previous_text = ""

    @QtCore.Slot()
    def on_text_change(self):
        if len(self.previous_text) < len(self.toPlainText()):
            if self.toPlainText()[-1] == '(':
                pair = ')'
                self.insertPlainText(pair)
                new_text_cursor = self.textCursor()
                new_text_cursor.setPosition(new_text_cursor.position() - 1)
                self.setTextCursor(new_text_cursor)

        self.previous_text = self.toPlainText()

        self.variable_button.variable_function(self.toPlainText())
        self.error_button.error_function(self.toPlainText())

    @QtCore.Slot()
    def on_cursor_change(self):
        self.label_line.line_and_column_number(self.textCursor())

    def change_size(self, mw: int, mh: int, max_: bool = True) -> None:
        if max_:
            self.setMaximumSize(mw, mh)
        else:
            self.setMinimumSize(mw, mh)

        return None

    def change_line_wrap(self) -> None:
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
