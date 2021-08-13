from PySide6 import QtWidgets


class CodeEditingField(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.current_text)

    def current_text(self) -> tuple:
        ret = (self.toPlainText(), self.toPlainText()[-1])
        return ret

    def change_max_size(self, mw: int, mh: int) -> None:
        self.setMaximumSize(mw, mh)
        return None
