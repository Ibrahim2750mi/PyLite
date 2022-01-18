from CodeEditingField import CodeEditingFieldWidget
from Preferences import PreferenceWidget
from TaskBar import TaskBarWidget
from UtilityBar import UtilityBarWidget

import pickle
import os
import subprocess as sp

from PySide6 import QtWidgets, QtCore, QtGui


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        self.task_bar = TaskBarWidget.TaskBarWidget(self)
        # setting up status bar
        self.status_bar = QtWidgets.QStatusBar(self.task_bar.get_main())
        self.status_bar.setStyleSheet(f"background: rgb(5, 122, 188)")
        self.setStatusBar(self.status_bar)

        # path of the current file
        self.path = None
        self.interpreter = "python3"

        # avoiding all pep-8 errors
        self.menu_bar = None
        self.file_menu = None
        self.edit_menu = None
        self.docker_menu = None
        self.build_menu = None

        self.right_docker = None
        self.right_docker_c = None
        self.central_widget = None
        self.preference_window = None
        self.preference_menu_bar = None
        self.preference_menu = None

        # main_field text
        self.text = ""

        self.initialise_attrs()
        self.initialise_right_docker()
        self.initialise_menu_bar()
        self.initialise_preference_window()
        self.setMenuBar(self.menu_bar)
        self.load_colors()
        self.path = None
        self.show()

    def dialog_critical(self, s):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.show()

    def run(self):
        self.file_save()
        output = sp.run([self.interpreter, self.path], capture_output=True)
        print(output.stdout.decode())

    def change_interpreter(self):
        self.interpreter, _ = QtWidgets.QInputDialog.getText(self,
                                                             "Change Python Interpreter",
                                                             "Enter the path of the python interpreter",
                                                             echo=QtWidgets.QLineEdit.Normal)

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
        print(path, "initial_path")
        if not path:
            return
        print(path, "still in front")
        self.__save_to_path(path)

    def __save_to_path(self, path):
        text = self.central_widget.get_main().toPlainText()
        try:
            print(path, "path reference")
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

    def on_preference_window(self):
        self.text = self.central_widget.code_editing_field.toPlainText()
        self.centralWidget().hide()
        self.menuBar().hide()
        self.removeDockWidget(self.right_docker)
        self.statusBar().hide()

        self.initialise_preference_window()
        self.load_colors()
        self.setCentralWidget(self.preference_window)
        self.setMenuBar(self.preference_menu_bar)

        self.menuBar().show()
        self.centralWidget().show()

    def on_main_window(self):
        self.centralWidget().hide()
        self.menuBar().hide()

        self.initialise_attrs()
        self.central_widget.code_editing_field.setPlainText(self.text)
        self.initialise_menu_bar()
        self.initialise_right_docker()
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.right_docker)
        self.setMenuBar(self.menu_bar)

        self.load_colors()
        self.central_widget.get_main().load_color()
        self.right_docker_c.get_docker().load_color()

        self.menuBar().show()
        self.centralWidget().show()
        self.statusBar().show()

    def load_colors(self):
        with open("../assets/assets.pickle", "rb") as f:
            colors = pickle.load(f)
            bg = colors["background"]
            fg = colors["foreground"]
        bg_rgb = list(int(bg[i:i + 2], 16) for i in (0, 2, 4))

        right_docker_color = self.color_initializer(16, bg_rgb)
        self.right_docker.setStyleSheet("QDockWidget:title {" + f"background: #{right_docker_color};" + "}")
        menu_bar_color = self.color_initializer(16, bg_rgb)
        self.menu_bar.setStyleSheet("QMenuBar {" + f"color: #{fg}; background-color: #{menu_bar_color};" + "}")
        self.preference_menu_bar.setStyleSheet("QMenuBar {" + f"color: #{fg}; "
                                                              f"background-color: #{menu_bar_color};" + "}")
        main_color = self.color_initializer(16, bg_rgb)
        self.setStyleSheet("QMainWindow {" + f"background: #{main_color};" + "}")

    @staticmethod
    def color_initializer(n: int, bg_rgb):
        for i, c in enumerate(bg_rgb):
            if c > n:
                bg_rgb[i] = c - n
        return '%02x%02x%02x' % tuple(bg_rgb)

    def initialise_menu_bar(self):
        # setting up menu-bar
        self.menu_bar = QtWidgets.QMenuBar()

        # setting up File Menu
        self.file_menu = self.menu_bar.addMenu("&File")

        open_file_action = QtGui.QAction("Open file", self)
        open_file_action.setStatusTip("Open file")
        open_file_action.setShortcut(QtGui.QKeySequence.Open)
        open_file_action.triggered.connect(self.file_open)
        self.file_menu.addAction(open_file_action)

        save_file_action = QtGui.QAction("Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.setShortcut(QtGui.QKeySequence.Save)
        save_file_action.triggered.connect(self.file_save)
        self.file_menu.addAction(save_file_action)

        saveas_file_action = QtGui.QAction("Save As", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.setShortcut(QtGui.QKeySequence.SaveAs)
        saveas_file_action.triggered.connect(self.file_saveas)
        self.file_menu.addAction(saveas_file_action)

        # setting up Edit Menu
        self.edit_menu = self.menu_bar.addMenu("&Edit")
        preferences_action = QtGui.QAction("Edit Preferences", self)
        preferences_action.setStatusTip("Here you can change  the background color/ foreground colors")
        preferences_action.triggered.connect(self.on_preference_window)
        self.edit_menu.addAction(preferences_action)

        # setting up Docker Buttons
        self.docker_menu = self.menu_bar.addMenu("&Docker&Utils")
        self.docker_menu.addAction(self.right_docker_c.get_variable_button())
        self.docker_menu.addAction(self.right_docker_c.get_error_button())

        # setting up Build menu
        self.build_menu = self.menu_bar.addMenu("&Build")

        run_action = QtGui.QAction("Run", self)
        run_action.setStatusTip("Runs the code")
        run_action.triggered.connect(self.run)
        self.build_menu.addAction(run_action)

        set_interpreter = QtGui.QAction("Set python interpreter", self)
        set_interpreter.setStatusTip("Changes the python interpreter")
        set_interpreter.triggered.connect(self.change_interpreter)
        self.build_menu.addAction(set_interpreter)

    def initialise_right_docker(self):
        self.right_docker = QtWidgets.QDockWidget()
        self.right_docker.setWidget(self.right_docker_c.get_docker())
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.right_docker)

    def initialise_attrs(self):
        self.right_docker_c = UtilityBarWidget.UtilityBarWidget()
        self.central_widget = CodeEditingFieldWidget.CodeFieldWidget(self.task_bar.get_main(),
                                                                     self.right_docker_c.get_variable_button(),
                                                                     self.right_docker_c.get_error_button(), self)

        self.setCentralWidget(self.central_widget.get_main())

    def initialise_preference_window(self):
        self.preference_window = PreferenceWidget.PreferenceWidget()
        self.preference_menu_bar = QtWidgets.QMenuBar()
        self.preference_menu = self.preference_menu_bar.addMenu("&Go Back")
        preference_go_back = QtGui.QAction("Back", self)
        preference_go_back.triggered.connect(self.on_main_window)
        self.preference_menu.addAction(preference_go_back)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setApplicationName("PyLite")
    window = Main()

    app.exec()
