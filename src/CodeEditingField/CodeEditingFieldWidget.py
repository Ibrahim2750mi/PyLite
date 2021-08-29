from CodeEditingMain import CodeEditingField, CodeEditingLayout

from PySide6 import QtWidgets, QtGui

import os
import sys

sys.path.append(os.path.realpath('.'))

from TaskBar.TaskBarLayout import TaskBarContent
from UtilityBar.UtilityBarLayout import UtilityButtons


class CodeFieldWidget(QtWidgets.QWidget):
    def __init__(self, line_labeler: TaskBarContent, variable_button: UtilityButtons,
                 error_button: UtilityButtons):
        super(CodeFieldWidget, self).__init__()
        self.code_editing_field = CodeEditingField.CodeEditingField(line_labeler, variable_button, error_button)
        self.code_editing_field.change_line_wrap()
        self.syntax_highlighter = CodeEditingLayout.CodeHighlightingField(self.code_editing_field)
        self.layout = CodeEditingLayout.CodeEditingLayout()
        self.layout.add(self.code_editing_field)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.code_editing_field.change_size(0.75 * self.size().width(), 0.85 * self.size().height())
        self.code_editing_field.setMinimumHeight(0.85 * self.size().height())
