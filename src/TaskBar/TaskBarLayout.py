from PySide6 import QtWidgets, QtCore, QtGui


class TaskBarLayout(QtWidgets.QHBoxLayout):
    def __init__(self):
        super(TaskBarLayout, self).__init__()
        self.setAlignment(QtCore.Qt.AlignBottom)

    def set_attributes(self, x: int, y: int) -> None:
        self.setContentsMargins(x, y, 0, 0)
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
