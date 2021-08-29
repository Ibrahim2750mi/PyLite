from .UtilityBarMain.UtilityBarLayout import UtilityButtons, UtilityBarLayout, UtilityDocker

from PySide6 import QtWidgets


class UtilityBarWidget(QtWidgets.QWidget):
    def __init__(self):
        super(UtilityBarWidget, self).__init__()
        self.docker = UtilityDocker()
        self.variable_button = UtilityButtons(1, self.docker)   # 1 = to check for variable
        self.error_button = UtilityButtons(2, self.docker)  # 2 = to check for errors
        self.layout = UtilityBarLayout()
        self.layout.add(self.variable_button)
        self.layout.add(self.error_button)
        self.layout.add(self.docker)

    def get_variable_button(self) -> UtilityButtons:
        return self.variable_button

    def get_error_button(self) -> UtilityButtons:
        return self.error_button
