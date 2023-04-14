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


    # Instantiate cursorManager
    # Instantiate UI
    # Instantiate Explain class

    #
    # # Build QEP tree by passing in the query as param
    # # Returns the root node of the QEP tree
    # QEPtree1 = explain.build_qep_tree(ui.getOldQueryInput())
    # QEPtree2 = explain.build_qep_tree(ui.getNewQueryInput())
    #
    # # Get explanation for specified query (q1 or q2) by passing in
    # # the root node of the respective QEP tree
    # # Returns List[str] of explanations
    # explanation = explain.get_QEP_explanation(QEPtree1)
    #
    # # Get the comparisons between 2 QEP
    # # by passing the 2 QEPtrees as params
    # # Returns List[str] of comparisons between the 2 QEPs
    # comparison = explain.get_QEP_comparison(QEPtree1, QEPtree2)
    #
    #
    # # Get visual plan of specified QEP
    # # by passing in the respective QEPtree that we want the visual plan for
    # # Returns List[str] representation of the tree
    # visualPlan = explain.get_visual_plan(QEPtree1)

    form.show()
    app.exec()

if __name__ == '__main__':
    main()

