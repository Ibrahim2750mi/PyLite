import sys
from PySide6 import QtCore, QtWidgets, QtGui
from CodeEditingField.CodeEditingField import CodeEditingField
from CodeEditingField.CodeEditingLayout import CodeEditingLayout, CodeHighlightingField


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.line_label = QtWidgets.QLabel()
        self.input_field = CodeEditingField(self.line_label)
        self.input_field.setTabStopDistance(10 + 10/3)
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
        self.layout.addWidget(self.line_label)

    def resizeEvent(self, event):
        self.input_field_layout.set_attributes(0, 0.16 * self.size().height())
        self.input_field.change_size(0.75 * self.size().width(), 0.74 * self.size().height())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
