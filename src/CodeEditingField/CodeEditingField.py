from PySide6 import QtWidgets


class CodeEditingField(QtWidgets.QTextEdit):
    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.current_text)

    def current_text(self) -> tuple:
        try:
            ret = (self.toPlainText(), self.toPlainText()[-1])
        except IndexError:
            return ()
        else:
            return ret

    def change_size(self, mw: int, mh: int, max_: bool = True) -> None:
        if max_:
            self.setMaximumSize(mw, mh)
        else:
            self.setMinimumSize(mw, mh)

        return None
