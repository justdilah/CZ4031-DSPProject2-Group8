import interface
from explain import *
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_material import apply_stylesheet
from matplotlib import pyplot as plt, patches


import psycopg2

class DatabaseCursor(object):
    def __init__(self, config):
        self.config = config

    def __enter__(self):
        self.conn = psycopg2.connect(
            host=self.config["host"],
            dbname=self.config["dbname"],
            user=self.config["user"],
            password=self.config["pwd"],
            port=self.config["port"]
        )
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

def main():
    app = QtWidgets.QApplication([])
    app.setStyle('Windows')

    apply_stylesheet(app, theme='dark_amber.xml')

    form = QtWidgets.QWidget()
    ui = interface.Ui_Form()
    ui.setupUi(form)

    cursorManager = CursorManager()
    explain = Explain(ui, cursorManager)


    form.show()
    app.exec()

if __name__ == '__main__':
    main()

