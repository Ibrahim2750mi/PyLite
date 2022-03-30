import pickle

from PySide6 import QtWidgets, QtCore

from TaskBar import TaskBarContent
from UtilityBar import UtilityActions


class CodeEditingField(QtWidgets.QPlainTextEdit):
    def __init__(self, line_labeler: TaskBarContent, variable_button: UtilityActions, error_button: UtilityActions,
                 window: QtWidgets.QMainWindow):
        super().__init__()
        self.textChanged.connect(self.on_text_change)
        self.cursorPositionChanged.connect(self.on_cursor_change)
        self.label_line = line_labeler
        self.variable_button = variable_button
        self.error_button = error_button
        self.window = window
        self.load_color()
        self.previous_text = ""

    @QtCore.Slot()
    def on_text_change(self):
        if len(self.previous_text) < len(self.toPlainText()):
            if self.toPlainText()[-1] in ('{', '[', '('):
                if self.toPlainText()[-1] == '(':
                    pair = ')'
                elif self.toPlainText()[-1] == '{':
                    pair = '}'
                elif self.toPlainText()[-1] == '[':
                    pair = ']'
                self.insertPlainText(pair)
                new_text_cursor = self.textCursor()
                new_text_cursor.setPosition(new_text_cursor.position() - 1)
                self.setTextCursor(new_text_cursor)

        self.previous_text = self.toPlainText()

        self.error_button.gen_info_function(self.toPlainText())
        self.variable_button.variable_function(self.toPlainText())
        self.window.file_save()

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

    def load_color(self):
        with open("../assets/assets.pickle", "rb") as f:
            colors = pickle.load(f)
            bg = colors["background"]
        self.setStyleSheet("QPlainTextEdit {" + f"background-color: #{bg};" + "}")
