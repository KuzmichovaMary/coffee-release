## maryshca

import sqlite3
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QTableWidget

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton


class FilmsLibrary(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.display_film_data()

    def display_film_data(self):
        query = """SELECT * FROM coffee"""
        res = self.connection.cursor().execute(query).fetchall()
        title = ["ID", "Сорт", "Степень обжарки", "молотый/в зернах", "описание вкуса", "цена", "объем упаковки"]
        self.tableWidget.setColumnCount(len(title))
        self.tableWidget.setHorizontalHeaderLabels(title)
        self.header = self.tableWidget.horizontalHeader()
        self.header.setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    win = FilmsLibrary()
    win.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
