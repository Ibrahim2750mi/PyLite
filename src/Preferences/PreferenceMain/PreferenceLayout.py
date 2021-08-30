import pickle
from string import hexdigits

from PySide6 import QtWidgets, QtCore


# formatting_type: Literal['string_formatting', 'function_formatting',
#                                                 'error_formatting', 'other_formatting',
#                                                 'decimal_formatting', 'background', 'foreground']


class PreferenceButtons(QtWidgets.QPushButton):
    def __init__(self, formatting_type: str, text: QtWidgets.QLineEdit):
        super(PreferenceButtons, self).__init__(text="Confirm")
        self.formatting_type = formatting_type
        self.text = text
        self.clicked.connect(self.on_click)

    @QtCore.Slot()
    def on_click(self):
        with open("../assets/assets.pickle", "rb") as f:
            current_styling = pickle.load(f)
        if self.__check(self.text.text().lower()):
            current_styling[self.formatting_type] = self.text.text().lower()
            with open("../assets/assets.pickle", "wb") as f:
                pickle.dump(current_styling, f)
        else:
            self.dialog_critical("Wrong hex format given")

    @staticmethod
    def __check(simplified_text: str) -> bool:
        for letter in simplified_text:
            if letter not in hexdigits:
                return False
        return True

    def dialog_critical(self, s):
        dlg = QtWidgets.QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QtWidgets.QMessageBox.Critical)
        dlg.show()


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
        self.button = PreferenceButtons(self.formatting_type, self.line_edit)
        self.addWidget(self.label)
        self.addWidget(self.line_edit)
        self.addWidget(self.button)

    def get_objects(self) -> tuple:
        return self.label, self.line_edit, self.button
