from .UtilityBarMain.UtilityBarLayout import UtilityActions, UtilityDocker

from PySide6 import QtWidgets


class UtilityBarWidget(QtWidgets.QWidget):
    def __init__(self):
        super(UtilityBarWidget, self).__init__()
        self.docker = UtilityDocker()
        self.docker.setReadOnly(True)
        self.variable_button = UtilityActions(1, self.docker, "Show Code info")  # 1 = to check for variable
        self.error_button = UtilityActions(2, self.docker, "Show General info")  # 2 = to check for errors

    def get_variable_button(self) -> UtilityActions:
        return self.variable_button

    def get_error_button(self) -> UtilityActions:
        return self.error_button

    def get_docker(self) -> UtilityDocker:
        return self.docker
