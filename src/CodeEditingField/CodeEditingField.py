from PySide6 import QtWidgets, QtCore
import ast


class CodeEditingField(QtWidgets.QPlainTextEdit):
    def __init__(self, line_labeler: QtWidgets.QLabel):
        super().__init__()
        self.textChanged.connect(self.on_text_change)
        self.variables = []
        self.label_line = line_labeler

    @QtCore.Slot()
    def on_text_change(self):
        try:
            st = ast.parse(self.toPlainText())
        except Exception as e:
            print(e)
        else:
            self.variables = []
            for node in ast.walk(st):
                if type(node) is ast.Name:
                    self.variables.append(node.id)
        lines = self.toPlainText().replace('\t', '    ').split('\n')
        counts_for_tabs = self.toPlainText().count('\t')
        column_number = 0
        line_number = 0
        cursor_pos = self.textCursor().position() + 4*counts_for_tabs
        print(cursor_pos, lines)

        for line in lines:
            if cursor_pos - len(line) >= 0:
                line_number += 1

            column_number = cursor_pos - len(' '.join(lines[0:line_number-1]))
        self.label_line.setText(f"line number:{line_number}, column number:{column_number}")

    def change_size(self, mw: int, mh: int, max_: bool = True) -> None:
        if max_:
            self.setMaximumSize(mw, mh)
        else:
            self.setMinimumSize(mw, mh)

        return None

    def change_line_wrap(self) -> None:
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
