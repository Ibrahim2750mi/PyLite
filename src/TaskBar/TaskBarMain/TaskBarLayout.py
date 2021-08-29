from PySide6 import QtWidgets, QtCore, QtGui


class TaskBarLayout(QtWidgets.QVBoxLayout):
    def __init__(self):
        super(TaskBarLayout, self).__init__()
        self.setAlignment(QtCore.Qt.AlignBottom)

    def set_attributes(self, x: int, y: int, dx: int = 0, dy: int = 0) -> None:
        self.setContentsMargins(x, y, dx, dy)
        return None

    def add(self, widget: QtWidgets.QLabel) -> None:
        self.addWidget(widget)
        return None


class TaskBarContent(QtWidgets.QLabel):
    def __init__(self, window: QtWidgets.QMainWindow):
        super(TaskBarContent, self).__init__()
        self.setAutoFillBackground(True)
        self.window = window

    def set_background_color(self, r, g, b):
        self.window.statusBar().setStyleSheet(f"background: rgb({r}, {g}, {b})")

    def line_and_column_number(self, cursor: QtGui.QTextCursor):
        column_number = cursor.columnNumber()
        line_number = cursor.blockNumber()
        self.set_background_color(137, 167, 178)
        self.window.statusBar().showMessage(f"line number:{line_number+1}, column number:{column_number+1}")
