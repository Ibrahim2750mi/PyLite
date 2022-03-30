from Preferences.PreferenceMain.PreferenceLayout import PreferenceLayout

import pickle

from PySide6 import QtWidgets, QtCore


class PreferenceWidget(QtWidgets.QWidget):
    def __init__(self):
        super(PreferenceWidget, self).__init__()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)

        # ------------------------------------------------------------
        self.background_layout = PreferenceLayout("Background Color:")
        self.foreground_layout = PreferenceLayout("Foreground Color:")
        self.function_layout = PreferenceLayout("Function-Formatting Color:")
        self.error_layout = PreferenceLayout("Error-Formatting Color:")
        self.other_layout = PreferenceLayout("Other-Formatting Color")
        self.decimal_layout = PreferenceLayout("Decimal-Formatting Color:")
        self.string_layout = PreferenceLayout("String-Formatting Color:")

        # ------------------------------------------------------------
        self.__add_widgets(self.background_layout, 0, 0)
        self.__add_widgets(self.foreground_layout, 0, 100)
        self.__add_widgets(self.function_layout, 0, 200)
        self.__add_widgets(self.error_layout, 3, 0)
        self.__add_widgets(self.other_layout, 3, 100)
        self.__add_widgets(self.decimal_layout, 3, 200)
        self.__add_widgets(self.string_layout, 6, 0)

        # ------------------------------------------------------------
        self.setLayout(self.main_layout)
        self.load_color()

    def __add_widgets(self, layout: PreferenceLayout, c: int, r: int):
        for i, widget in enumerate(layout.get_objects(), start=1):
            self.main_layout.addWidget(widget, (c+i)*10, r, 2, 2)
            self.setLayout(self.main_layout)

    def load_color(self):
        with open("../assets/assets.pickle", "rb") as f:
            colors = pickle.load(f)
            bg = colors["background"]
            fg = colors["foreground"]
        self.setStyleSheet("QWidget {" + f"color: #{fg}; background-color: #{bg};" + "}")
