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
    def __init__(self):
        super(TaskBarContent, self).__init__()
        self.setAutoFillBackground(True)

    @staticmethod
    def __auto_color_maker(r, g, b):
        color = QtGui.QColor(r, g, b)
        return color

    def set_background_color(self, r, g, b):
        color = self.__auto_color_maker(r, g, b)
        color_palette = QtGui.QPalette()
        color_palette.setColor(QtGui.QPalette.Window, color)
        self.setPalette(color_palette)

    def set_foreground_color(self, r, g, b):
        color = self.__auto_color_maker(r, g, b)
        color_palette = QtGui.QPalette()
        color_palette.setColor(QtGui.QPalette.WindowText, color)
        self.setPalette(color_palette)

    def line_and_column_number(self, cursor: QtGui.QTextCursor):
        column_number = cursor.columnNumber()
        line_number = cursor.blockNumber()
        self.setText(f"line number:{line_number+1}, column number:{column_number+1}")
