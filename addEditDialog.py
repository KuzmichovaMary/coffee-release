import sqlite3

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton


class FilmAddDialog(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("addEditCoffeeForm.ui", self)
        self.accepted = 0
        self.pushButton.clicked.connect(self.get_data)
        self.make_combo_box()

    def make_combo_box(self):
        for genre in ["В зернах", "Молотый"]:
            self.beans.addItem(genre)

    def get_data(self):
        self.s = self.sort.text()
        self.r = str(self.roast.value())
        self.b = "True" if self.beans.currentText() == "В зернах" else "False"
        self.t = self.taste.text()
        self.p = int(self.price.value())
        self.v = int(self.volume.value())
        self.accepted = 1
        self.accept()

    def exec_(self):
        super(FilmAddDialog, self).exec_()
        if self.accepted:
            return 1, self.s, self.r, self.b, self.t, self.p, self.v
        else:
            return 0,


class FilmEditDialog(FilmAddDialog):
    def __init__(self, sort, roast, beans, taste, price, volume):
        super().__init__()
        self.setWindowTitle("Редактирование фильма")
        self.sort.setText(sort)
        self.roast.setValue(int(roast))
        self.beans.setCurrentText("Да" if beans else "Нет")
        self.taste.setText(taste)
        self.price.setValue(int(price))
        self.volume.setValue(int(volume))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    class Window(QMainWindow):
        def __init__(self):
            super().__init__()
            self.centralWidget = QPushButton("test")
            self.centralWidget.clicked.connect(self.film_testing)
            self.setCentralWidget(self.centralWidget)

        def film_testing(self):
            dlg = FilmAddDialog()
            print(dlg.exec_())


    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())