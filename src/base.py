import sys
from PySide6 import QtWidgets, QtCore
from CodeEditingField.CodeEditingField import CodeEditingField
from TaskBar.TaskBarLayout import TaskBarLayout, TaskBarContent
from CodeEditingField.CodeEditingLayout import CodeEditingLayout, CodeHighlightingField
from UtilityBar.UtilityBarLayout import UtilityDocker, UtilityButtons, UtilityBarLayout


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)

        self.task_bar_layout = TaskBarLayout()
        self.task_bar_line_label = TaskBarContent()
        self.task_bar_line_label.setWordWrap(True)
        self.task_bar_line_label.set_background_color(137, 167, 178)
        # self.task_bar_layout.set_attributes(5, 0.9 * self.size().height())
        self.task_bar_layout.add(self.task_bar_line_label)

        self.side_bar_layout_docker = UtilityBarLayout()
        self.side_bar_docker = UtilityDocker()
        # self.side_bar_docker.change_line_wrap()
        self.side_bar_docker.setReadOnly(True)
        self.side_bar_layout_docker.add(self.side_bar_docker)

        self.side_bar_variable_button = UtilityButtons(1, self.side_bar_docker)
        self.side_bar_variable_button.setText("Show Variables")
        self.side_bar_layout_button_variable = UtilityBarLayout()
        self.side_bar_layout_button_variable.add(self.side_bar_variable_button)

        self.side_bar_error_button = UtilityButtons(2, self.side_bar_docker)
        self.side_bar_error_button.setText("Show Errors")
        self.side_bar_layout_button_error = UtilityBarLayout()
        self.side_bar_layout_button_error.add(self.side_bar_error_button)

        self.input_field = CodeEditingField(self.task_bar_line_label, self.side_bar_variable_button, self.side_bar_error_button)
        self.input_field.setTabStopDistance(10 + 10 / 3)
        self.input_field.change_line_wrap()
        self.input_field_highlighter = CodeHighlightingField(self.input_field)

        self.input_field_layout = CodeEditingLayout()
        self.input_field.change_size(400, 444, False)
        self.input_field_layout.set_attributes(0, 0.16 * self.size().height())

        self.input_field_layout.add(self.input_field)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.addLayout(self.input_field_layout, 0, 0, 50, 600)
        self.layout.addLayout(self.side_bar_layout_button_variable, 0, 590, 15, 100)
        self.layout.addLayout(self.side_bar_layout_button_error, 0, 590, 30, 100)
        self.layout.addLayout(self.side_bar_layout_docker, 10, 580, 100, 160)
        # self.layout.addLayout(self.sub_layout)
        self.layout.addLayout(self.task_bar_layout, 999, 15, 10, 20)


    def resizeEvent(self, event):
        # self.side_bar_layout_docker_variable.set_attributes(0.8 * self.size().width(),20)
        self.side_bar_docker.change_size(0.18 * self.size().width(), 0.6 * self.size().height())
        # self.side_bar_variable_button.change_size(0.1*self.size().width(), 0.15*self.size().height())
        self.input_field_layout.set_attributes(0, 0.05 * self.size().height())
        self.input_field.change_size(0.75 * self.size().width(), 0.85 * self.size().height())
        self.input_field.setMinimumHeight(0.85 * self.size().height())
        

        # self.task_bar_layout.set_attributes(0, 0, dx=0.75 * self.size().width(),
        #                                     dy=self.size().height())
        self.task_bar_line_label.setFixedSize(0.5 * self.size().width(), 25)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
