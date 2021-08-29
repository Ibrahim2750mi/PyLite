from .TaskBarMain.TaskBarLayout import TaskBarContent

from PySide6 import QtWidgets, QtGui


class TaskBarWidget(QtWidgets.QWidget):
    def __init__(self, window: QtWidgets.QMainWindow):
        super(TaskBarWidget, self).__init__()
        self.task_bar_line_label = TaskBarContent(window)
        self.task_bar_line_label.setWordWrap(True)
        self.task_bar_line_label.set_background_color(137, 167, 178)
    
    def get_main(self) -> TaskBarContent:
        return self.task_bar_line_label

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.task_bar_line_label.setFixedSize(0.5 * self.size().width(), 25)
