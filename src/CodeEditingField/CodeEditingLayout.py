from PySide6 import QtWidgets, QtCore


class CodeEditingLayout(QtWidgets.QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignTop)

    def set_attributes(self, x: int, y: int) -> None:
        self.setContentsMargins(x, y, 0, 0)
        return None

    def add(self, widget: QtWidgets.QLineEdit) -> None:
        self.addWidget(widget)
        return None
