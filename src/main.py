from CodeEditingField import CodeEditingFieldWidget
from TaskBar import TaskBarWidget
from UtilityBar import UtilityBarWidget

import os

from PySide6 import QtWidgets, QtCore, QtGui


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

        # setting up menu-bar
        # setting up File Menu
        self.file_menu = self.menuBar().addMenu("&File")
        open_file_action = QtGui.QAction("Open file", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        self.file_menu.addAction(open_file_action)

        save_file_action = QtGui.QAction("Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        self.file_menu.addAction(save_file_action)

        saveas_file_action = QtGui.QAction("Save As", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        self.file_menu.addAction(saveas_file_action)

        # setting up Edit Menu
        self.edit_menu = self.menuBar().addMenu("&Edit")
        preferences_action = QtGui.QAction("Edit Preferences", self)
        preferences_action.setStatusTip("Here you can change  the background color/ foreground colors")
        preferences_action.triggered.connect(self.test)
        self.edit_menu.addAction(preferences_action)

        self.path = None
        self.show()

    def dialog_critical(self, s):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open file", "",
                                                        "All files (*.*)")
        if path:
            try:
                with open(path) as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))
            else:
                self.path = path
                self.central_widget.get_main().setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path is None:
            return self.file_saveas()
        self.__save_to_path(self.path)

    def file_saveas(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save file", "",
                                                        "All files (*.*)")
        if not path:
            return
        self.__save_to_path(path)

    def __save_to_path(self, path):
        text = self.central_widget.get_main().toPlainText()
        try:
            with open(path, 'w') as f:
                f.write(text)
        except Exception as e:
            self.dialog_critical(str(e))
        else:
            self.path = path
            self.update_title()

    def update_title(self):
        self.setWindowTitle("%s - PyLite" % (os.path.basename(self.path)
                                             if self.path else "Untitled"))

    def test(self):
        self.centralWidget().hide()
        self.menuBar().hide()
        self.removeDockWidget(self.right_docker)
        self.statusBar().hide()
        self.removeToolBar(self.tool_bar)

        new_widget = QtWidgets.QWidget()
        new_layout = QtWidgets.QGridLayout()
        new_label = QtWidgets.QLabel()
        new_label.setText("bg color")
        new_line_text = QtWidgets.QLineEdit()
        new_layout.addWidget(new_label, 0, 1)
        new_layout.addWidget(new_line_text, 1, 1)
        new_widget.setLayout(new_layout)
        self.setCentralWidget(new_widget)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setApplicationName("PyLite")
    window = Main()

    app.exec()
