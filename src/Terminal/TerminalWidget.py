from pathlib import Path
import pickle


from PySide6 import QtWidgets

from Terminal import Terminal


class TerminalWidget(QtWidgets.QWidget):
    def __init__(self, path):
        super(TerminalWidget, self).__init__()
        self._docker = Terminal(path or str(Path().home().absolute()))

    @property
    def docker(self):
        return self._docker

    def load_color(self):
        with open("../assets/assets.pickle", "rb") as f:
            colors = pickle.load(f)
            bg = colors["background"]
            fg = colors["foreground"]
        self._docker.setStyleSheet("QTextEdit {" + f"color: #{fg};background-color: #{bg};" + "}")
