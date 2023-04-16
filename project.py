import interface
from explain import *
from PyQt5 import QtCore, QtGui, QtWidgets
from qt_material import apply_stylesheet

def main():
    app = QtWidgets.QApplication([])
    app.setStyle('Windows')

    apply_stylesheet(app, theme='dark_amber.xml')

    form = QtWidgets.QWidget()


    cursorManager = CursorManager()
    explain = Explain(cursorManager)

    ui = interface.Ui_Form()
    ui.setupUi(form, explain)

    # SET DATABASE SCHEMAs
    ui.setSchema()

    form.show()
    app.exec()

if __name__ == '__main__':
    main()

