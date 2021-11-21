import re
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
    
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == 16777220:
            # enter
            output = subprocess.run(self.current_text.split(' '), capture_output=True)
            self.setPlainText(self.toPlainText()+"\n" + output.stdout.decode() + "\n" + self.path+"$")
            self.__auto_cursor()

            self.cmds.append(self.current_text)
            self.current_text = ""

        elif e.key() == 16777219:
            # backspace
            deletable_text_regex = self.path + r"\$|.*?"
            if self.toPlainText()[-1] in [x for x in re.findall(deletable_text_regex, self.toPlainText()) if x]:
                self.setPlainText(self.toPlainText()[0:-1])

                self.__auto_cursor()

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
                self.__auto_cursor()

        else:
            self.setPlainText(self.toPlainText()+e.text())
            self.current_text += e.text()
            k = self.textCursor()
            k.setPosition(len(self.toPlainText()), QtGui.QTextCursor.MoveAnchor)
            self.setTextCursor(k)

    def initialise_new_line(self) -> None:

        self.setPlainText(f"{self.path}$")
        self.__auto_cursor()

    def __auto_cursor(self, pt=None) -> None:
        if not pt:
            pt = len(self.toPlainText())
        cur = self.textCursor()
        cur.setPosition(pt)
        self.setTextCursor(cur)
