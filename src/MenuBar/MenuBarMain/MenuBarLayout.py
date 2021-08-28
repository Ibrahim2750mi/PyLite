from PySide6 import QtWidgets, QtCore
import os
import sys

sys.path.append(os.path.realpath('.'))
from CodeEditingField.CodeEditingField import CodeEditingField


class MenuBarLayout(QtWidgets.QHBoxLayout):
    def __init__(self):
        super(MenuBarLayout, self).__init__()
        self.setAlignment(QtCore.Qt.AlignTop)

    def set_attributes(self, x: int, y: int, dx: int = 0, dy: int = 0) -> None:
        self.setContentsMargins(x, y, dx, dy)
        return None

    def add(self, widget: QtWidgets.QLabel) -> None:
        self.addWidget(widget)
        return None


class FileMenu(QtWidgets.QMenu):
    def __init__(self, text: CodeEditingField, main_layout: QtWidgets.QGridLayout):
        super(FileMenu, self).__init__()
        self.triggered.connect(self.on_action)
        self.text = text
        self.main_layout = main_layout

    def on_action(self, action):
        print(self.text.toPlainText())


class FileButton(QtWidgets.QPushButton):
    def __init__(self, menu: FileMenu):
        super(FileButton, self).__init__("File")
        self.menu_bar = menu
        self.clicked.connect(self.on_click)

    def on_click(self):
        self.menu_bar.exec(self.mapToGlobal(QtCore.QPoint(100, 10)))
