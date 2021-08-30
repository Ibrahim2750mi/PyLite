import pickle

from PySide6 import QtWidgets, QtCore

# formatting_type: Literal['string_formatting', 'function_formatting',
#                                                 'error_formatting', 'other_formatting',
#                                                 'decimal_formatting', 'background', 'foreground']


class PreferenceButtons(QtWidgets.QPushButton):
    def __init__(self, formatting_type: str, color: str):
        super(PreferenceButtons, self).__init__(text="Confirm")
        self.formatting_type = formatting_type
        self.color = color
        self.clicked.connect(self.on_click)

    @QtCore.Slot()
    def on_click(self):
        with open("../assets/assets.pickle", "rb") as f:
            current_styling = pickle.load(f)
        current_styling[self.formatting_type] = self.color
        with open("../assets/assets.pickle", "wb") as f:
            pickle.dump(current_styling, f)


class PreferenceLayout(QtWidgets.QVBoxLayout):
    def __init__(self, label_text: str):
        super(PreferenceLayout, self).__init__()
        self.setAlignment(QtCore.Qt.AlignTop)
        self.label = QtWidgets.QLabel(text=label_text)

        self.formatting_type = label_text.split(' Color')[0].lower().replace("-", "_")

        with open("../assets/assets.pickle", "rb") as f:
            self.line_edit_text = pickle.load(f)[self.formatting_type]
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setText(self.line_edit_text)
        self.line_edit.setFixedWidth(60)
        self.button = PreferenceButtons(self.formatting_type, self.line_edit_text)
        self.addWidget(self.label)
        self.addWidget(self.line_edit)
        self.addWidget(self.button)

    def get_objects(self) -> tuple:
        return self.label, self.line_edit, self.button
