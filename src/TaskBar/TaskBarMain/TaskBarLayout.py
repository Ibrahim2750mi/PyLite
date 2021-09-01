from PySide6 import QtWidgets, QtGui


class TaskBarContent(QtWidgets.QLabel):
    def __init__(self, window: QtWidgets.QMainWindow):
        super(TaskBarContent, self).__init__()
        self.setAutoFillBackground(True)
        self.window = window

    def line_and_column_number(self, cursor: QtGui.QTextCursor):
        column_number = cursor.columnNumber()
        line_number = cursor.blockNumber()
        self.window.statusBar().showMessage(f"line number:{line_number+1}, column number:{column_number+1}")
