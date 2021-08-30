import os
import sys

from PySide6 import QtWidgets, QtGui

from .CodeEditingMain import CodeEditingField, CodeEditingLayout

sys.path.append(os.path.realpath('.'))

from TaskBar.TaskBarMain.TaskBarLayout import TaskBarContent
from UtilityBar.UtilityBarMain.UtilityBarLayout import UtilityButtons


class CodeFieldWidget(QtWidgets.QWidget):
    def __init__(self, line_labeler: TaskBarContent, variable_button: UtilityButtons,
                 error_button: UtilityButtons):
        super(CodeFieldWidget, self).__init__()
        self.code_editing_field = CodeEditingField.CodeEditingField(line_labeler, variable_button, error_button)
        self.code_editing_field.setTabStopDistance(40/3)
        self.code_editing_field.change_line_wrap()
        self.syntax_highlighter = CodeEditingLayout.CodeHighlightingField(self.code_editing_field)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.code_editing_field.change_size(0.75 * self.size().width(), 0.85 * self.size().height())
        self.code_editing_field.setMinimumHeight(0.85 * self.size().height())

    def get_main(self) -> CodeEditingField.CodeEditingField:
        return self.code_editing_field
