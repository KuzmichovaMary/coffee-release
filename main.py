## maryshca

import sqlite3
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QTableWidget

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from addEditDialog import FilmAddDialog, FilmEditDialog


class FilmsLibrary(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("main.ui", self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.display_film_data()
        self.pushButton.clicked.connect(self.add_film)
        self.pushButton_2.clicked.connect(self.edit_film)

    def is_one_row_selected(self):
        if self.tableWidget.selectedItems():
            a = self.tableWidget.selectedItems()[0].row()
            for i in self.tableWidget.selectedItems():
                row, column = i.row(), i.column()
                if row != a:
                    return False,
            return True, self.tableWidget.selectedItems()[0].text()
        return False,

    def edit_film(self):
        a = self.is_one_row_selected()
        if a[0]:
            arr = self.connection.execute(f"select * from coffee where id = {int(a[1])}").fetchone()
            id = arr[0]
            arr = FilmEditDialog(arr[1], arr[2], arr[3], arr[4], arr[5], arr[6]).exec_()
            if arr[0]:
                query = f"""update coffee
                            set
                            Sort = '{arr[1]}',
                            Roasting = '{arr[2]}',
                            Beans = {arr[3]},
                            Taste = '{arr[4]}',
                            Price = {arr[5]},
                            Volume = {arr[6]}
                            where id = {id}"""
                self.connection.execute(query)
                self.connection.commit()
                self.display_film_data()
        else:
            self.statusbar.setStatusTip("Нет выбранного фильма.")

    def add_film(self):
        arr = FilmAddDialog().exec_()
        if arr[0]:
            query = f"""INSERT INTO coffee(Sort, Roasting, Beans, Taste, Price, Volume)
             VALUES('{arr[1]}', '{arr[2]}', {arr[3]}, '{arr[4]}', {arr[5]}, {arr[6]})"""
            self.connection.execute(query)
            self.connection.commit()
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
