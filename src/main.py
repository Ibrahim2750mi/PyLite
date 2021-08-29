from CodeEditingField import CodeEditingFieldWidget
from TaskBar import TaskBarWidget
from UtilityBar import UtilityBarWidget

from PySide6 import QtWidgets


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.task_bar = TaskBarWidget.TaskBarWidget(self)
        self.right_docker = UtilityBarWidget.UtilityBarWidget()
        self.central_widget = CodeEditingFieldWidget.CodeFieldWidget(self.task_bar.get_main(),
                                                                     self.right_docker.get_variable_button(),
                                                                     self.right_docker.get_error_button())
        self.status_bar = QtWidgets.QStatusBar(self.task_bar.get_main())
        self.setCentralWidget(self.central_widget.get_main())
        self.setStatusBar(self.status_bar)
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setApplicationName("PyQt5-Note")
    window = Main()

    app.exec()
