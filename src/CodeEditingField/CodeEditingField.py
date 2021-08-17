from PySide6 import QtWidgets


class CodeEditingField(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()

    def change_size(self, mw: int, mh: int, max_: bool = True) -> None:
        if max_:
            self.setMaximumSize(mw, mh)
        else:
            self.setMinimumSize(mw, mh)

        return None

    def change_line_wrap(self) -> None:
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
