import sys
from PySide6 import QtCore, QtWidgets, QtGui
from CodeEditingField.CodeEditingField import CodeEditingField
from CodeEditingField.CodeEditingLayout import CodeEditingLayout


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(800, 600)
        self.input_field = CodeEditingField()
        # self.input_field.setTextColor(QtGui.QColor(255, 0, 0))
        self.input_field_layout = CodeEditingLayout()
        # self.input_field.change_size(683, 520.96)
        self.input_field.change_size(400, 444, False)
        self.input_field_layout.set_attributes(0.25 * self.size().width(), 0.16 * self.size().height())
        self.input_field_layout.add(self.input_field)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.input_field_layout)

    def resizeEvent(self, event):
        self.input_field_layout.set_attributes(0.25 * self.size().width(), 0.16 * self.size().height())
        self.input_field.change_size(0.5 * self.size().width(), 0.74 * self.size().height())


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
