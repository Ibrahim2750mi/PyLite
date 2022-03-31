import functools
import re
import pathlib
import shlex
import subprocess

from PySide6 import QtWidgets, QtGui


class str(str):
    def __init__(self, arg):
        super(str, self).__init__()

    def __str__(self):
        return str(self)

    def __sub__(self, other):
        if other in self:
            if self.count(other) == 1:
                return self.replace(other, "")
            else:
                new_var = (self.split(other))
                temp_del_item = new_var.pop(-1)
                return other.join(new_var) + temp_del_item
        else:
            raise TypeError("unsupported operand type(s) for -: 'str' and 'str'")

    def __isub__(self, other):
        return self.__sub__(other)


class Terminal(QtWidgets.QTextEdit):
    def __init__(self, path):
        super(Terminal, self).__init__()
        self.current_text = ""
        self.path = path
        self.initialise_new_line()
        self.cmds = []
        self.path_history = [path]

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == 16777220:
            # enter
            cmd = shlex.split(self.current_text)
            popen = functools.partial(subprocess.Popen, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1)
            try:
                proc = popen(cmd, cwd=self.path)
            except FileNotFoundError:
                print(cmd)
                if "source" in cmd:
                    try:
                        cmd[cmd.index("source") + 1] = "source " + cmd[cmd.index("source") + 1]
                        _ = cmd.pop(cmd.index("source"))
                    except IndexError:
                        pass
                proc = popen(['bash', '-c'] + cmd, cwd=self.path)

            self.setPlainText(self.toPlainText() + "\n")
            for line in proc.stdout.readlines():
                self.setPlainText(self.toPlainText() + line)
                self._auto_cursor()

            if cmd[0] == "cd":
                if pathlib.Path(cmd[-1]).exists():
                    self.change_path(cmd[-1])
                    self.path_history.append(self.path)
                else:
                    if pathlib.Path(self.path + cmd[-1]).exists():
                        self.change_path(self.path + cmd[-1])
                        self.path_history.append(self.path)
                    else:
                        self.setPlainText(self.toPlainText() + "No such file or directory\n")
                        self.setPlainText(self.toPlainText() + self.path + "$")
                        self._auto_cursor()
            else:
                self.setPlainText(self.toPlainText() + self.path + "$")
                self._auto_cursor()
            self.cmds.append(self.current_text)
            self.current_text = ""

        elif e.key() == 16777219:
            # backspace
            deletable_text_regex = ""

            for path in self.path_history:
                deletable_text_regex += "(" + path + r"\$|.*?)|"
            deletable_text_regex += "(.*?)"

            if self.toPlainText()[-1] in [x[0] for x in re.findall(deletable_text_regex, self.toPlainText()) if x[0]]:
                self.setPlainText(self.toPlainText()[0:-1])

                self._auto_cursor()

                self.current_text = self.current_text[0:-1]

        elif e.key() == 16777235:
            # up
            try:
                temp_text = str(self.toPlainText()) - str(self.current_text)
            except ValueError:
                temp_text = self.toPlainText()
            try:
                self.setPlainText(temp_text + self.cmds[-1])
            except IndexError:
                pass
            else:
                self.current_text = self.cmds[-1]
                self._auto_cursor()

        else:
            self.setPlainText(self.toPlainText() + e.text())
            self.current_text += e.text()
            temp_text_cursor = self.textCursor()
            temp_text_cursor.setPosition(len(self.toPlainText()), QtGui.QTextCursor.MoveAnchor)
            self.setTextCursor(temp_text_cursor)

    def initialise_new_line(self) -> None:

        self.setPlainText(f"{self.path}$")
        self._auto_cursor()

    def _auto_cursor(self, pt=None) -> None:
        if not pt:
            pt = len(self.toPlainText())
        cur = self.textCursor()
        cur.setPosition(pt)
        self.setTextCursor(cur)

    def change_path(self, path: str):
        self.path = path
        if not self.path.endswith("/"):
            self.path += "/"
        self.setPlainText(self.toPlainText() + "\n")
        self.setPlainText(self.toPlainText() + self.path + "$")
        self._auto_cursor()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    app.setApplicationName("PyLite")
    k = Terminal('/home/ibrahim/')
    k.show()
    app.exec()
