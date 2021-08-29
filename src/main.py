from CodeEditingField import CodeEditingFieldWidget
from TaskBar import TaskBarWidget
from UtilityBar import UtilityBarWidget

from PySide6 import QtWidgets, QtCore


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.task_bar = TaskBarWidget.TaskBarWidget(self)
        self.right_docker_c = UtilityBarWidget.UtilityBarWidget()
        self.central_widget = CodeEditingFieldWidget.CodeFieldWidget(self.task_bar.get_main(),
                                                                     self.right_docker_c.get_variable_button(),
                                                                     self.right_docker_c.get_error_button())

        self.setCentralWidget(self.central_widget.get_main())

        # setting up status bar
        self.status_bar = QtWidgets.QStatusBar(self.task_bar.get_main())
        self.setStatusBar(self.status_bar)

        # setting up docker
        self.right_docker = QtWidgets.QDockWidget()
        self.right_docker.setWidget(self.right_docker_c.get_docker())
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.right_docker)

        # setting up toolbar
        self.tool_bar = QtWidgets.QToolBar()
        self.tool_bar.addWidget(self.right_docker_c.get_variable_button())
        self.tool_bar.addWidget(self.right_docker_c.get_error_button())
        self.addToolBar(self.tool_bar)
        # self.tool_bar.actionTriggered.connect(self.test)
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setApplicationName("PyQt5-Note")
    window = Main()

    app.exec()
