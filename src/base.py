import sys
from PySide6 import QtWidgets
from CodeEditingField.CodeEditingField import CodeEditingField
from CodeEditingField.CodeEditingLayout import CodeEditingLayout, CodeHighlightingField
from TaskBar.TaskBarLayout import TaskBarLayout, TaskBarContent


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.task_bar_layout = TaskBarLayout()
        self.task_bar_line_label = TaskBarContent()
        self.task_bar_line_label.set_background_color(137, 167, 178)
        self.task_bar_layout.add(self.task_bar_line_label)
        self.input_field = CodeEditingField(self.task_bar_line_label)
        self.input_field.setTabStopDistance(10 + 10 / 3)
        self.input_field.change_line_wrap()
        self.input_field_highlighter = CodeHighlightingField(self.input_field)
        # self.input_field.setTextColor(QtGui.QColor(255, 0, 0))
        self.input_field_layout = CodeEditingLayout()
        # self.input_field.change_size(683, 520.96)
        self.input_field.change_size(400, 444, False)
        self.input_field_layout.set_attributes(0, 0.16 * self.size().height())
        self.input_field_layout.add(self.input_field)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.input_field_layout)
        self.layout.addLayout(self.task_bar_layout)

    def resizeEvent(self, event):
        self.input_field_layout.set_attributes(0, 0.16 * self.size().height())
        self.input_field.change_size(0.75 * self.size().width(), 0.74 * self.size().height())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
