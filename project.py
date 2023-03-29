import interface
from explain import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow

def main():
    app = QtWidgets.QApplication([])
    form = QtWidgets.QWidget()
    ui = interface.Ui_Form()
    ui.setupUi(form)
    cursorManager = CursorManager()
    explain = Explain(ui, cursorManager)
    form.show()
    app.exec()

if __name__ == '__main__':
    main()

