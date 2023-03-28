from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("CZ4031-Group8-DSPProject2")
        Form.resize(1165, 779)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 1141, 721))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.mainHorizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.mainHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.mainHorizontalLayout.setObjectName("mainHorizontalLayout")
        self.LeftLayout = QtWidgets.QVBoxLayout()
        self.LeftLayout.setObjectName("LeftLayout")

        # -------------------------- DATABASE SCHEMA -----------------------------------------
        # Label
        self.schemaLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.schemaLabel.setObjectName("schemaLabel")
        self.LeftLayout.addWidget(self.schemaLabel)

        # QTreeWidget
        self.databaseSchema = QTreeWidget(self.horizontalLayoutWidget_2)
        self.databaseSchema.setObjectName(u"databaseSchema")
        self.databaseSchema.setHeaderLabels(["Schema"])

        self.LeftLayout.addWidget(self.databaseSchema)
        self.LeftLayout.addWidget(self.databaseSchema)
        self.mainHorizontalLayout.addLayout(self.LeftLayout)
        self.RightLayout = QtWidgets.QVBoxLayout()
        self.RightLayout.setObjectName("RightLayout")
        self.TopLayout = QtWidgets.QHBoxLayout()
        self.TopLayout.setObjectName("TopLayout")

        # -------------------------- OLD QUERY -----------------------------------------
        self.OldQueryLayout = QtWidgets.QVBoxLayout()
        self.OldQueryLayout.setObjectName("OldQueryLayout")

        # Label
        self.oldQueryLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.oldQueryLabel.setObjectName("oldQueryLabel")
        self.OldQueryLayout.addWidget(self.oldQueryLabel)

        # Old Query Input
        self.oldQueryInput = QtWidgets.QTextBrowser(self.horizontalLayoutWidget_2)
        self.oldQueryInput.setObjectName("oldQueryInput")
        self.oldQueryInput.setReadOnly(False)

        self.OldQueryLayout.addWidget(self.oldQueryInput)

        # Old Query Button
        self.oldQueryButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.oldQueryButton.setObjectName("oldQueryButton")
        self.OldQueryLayout.addWidget(self.oldQueryButton)
        self.TopLayout.addLayout(self.OldQueryLayout)
        self.oldQEPLayout = QtWidgets.QVBoxLayout()
        self.oldQEPLayout.setObjectName("oldQEPLayout")
        self.oldQEPLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.oldQEPLabel.setObjectName("oldQEPLabel")
        self.oldQEPLayout.addWidget(self.oldQEPLabel)

        # Display Old QEP Plan
        self.oldQEPOutput = QtWidgets.QTextBrowser(self.horizontalLayoutWidget_2)
        self.oldQEPOutput.setObjectName("oldQEPOutput")
        self.oldQEPLayout.addWidget(self.oldQEPOutput)
        self.TopLayout.addLayout(self.oldQEPLayout)
        self.oldVisualLayout = QtWidgets.QVBoxLayout()
        self.oldVisualLayout.setObjectName("oldVisualLayout")
        self.oldVisualLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.oldVisualLabel.setObjectName("oldVisualLabel")
        self.oldVisualLayout.addWidget(self.oldVisualLabel)

        # Display Old Visual Plan
        self.oldGraphicsView = QtWidgets.QGraphicsView(self.horizontalLayoutWidget_2)
        self.oldGraphicsView.setObjectName("oldGraphicsView")
        self.oldVisualLayout.addWidget(self.oldGraphicsView)
        self.TopLayout.addLayout(self.oldVisualLayout)
        self.RightLayout.addLayout(self.TopLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # -------------------------- NEW QUERY -----------------------------------------
        self.NewQueryLayout = QtWidgets.QVBoxLayout()
        self.NewQueryLayout.setObjectName("NewQueryLayout")

        # Label
        self.newQueryLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.newQueryLabel.setObjectName("newQueryLabel")
        self.NewQueryLayout.addWidget(self.newQueryLabel)

        # New Query Input
        self.newQueryInput = QtWidgets.QTextBrowser(self.horizontalLayoutWidget_2)
        self.newQueryInput.setObjectName("newQueryInput")
        self.newQueryInput.setReadOnly(False)
        self.NewQueryLayout.addWidget(self.newQueryInput)

        # New Query Button
        self.newQueryButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.newQueryButton.setObjectName("newQueryButton")
        self.NewQueryLayout.addWidget(self.newQueryButton)
        self.horizontalLayout_2.addLayout(self.NewQueryLayout)
        self.newQEPLayout = QtWidgets.QVBoxLayout()
        self.newQEPLayout.setObjectName("newQEPLayout")
        self.newQEPLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.newQEPLabel.setObjectName("newQEPLabel")
        self.newQEPLayout.addWidget(self.newQEPLabel)

        # Display New QEP Plan
        self.newQEPOutput = QtWidgets.QTextBrowser(self.horizontalLayoutWidget_2)
        self.newQEPOutput.setObjectName("newQEPOutput")
        self.newQEPLayout.addWidget(self.newQEPOutput)
        self.horizontalLayout_2.addLayout(self.newQEPLayout)
        self.newVisualLayout = QtWidgets.QVBoxLayout()
        self.newVisualLayout.setObjectName("newVisualLayout")
        self.newVisualLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.newVisualLabel.setObjectName("newVisualLabel")
        self.newVisualLayout.addWidget(self.newVisualLabel)

        # Display New Visual Plan
        self.newGraphicsView = QtWidgets.QGraphicsView(self.horizontalLayoutWidget_2)
        self.newGraphicsView.setObjectName("newGraphicsView")
        self.newVisualLayout.addWidget(self.newGraphicsView)
        self.horizontalLayout_2.addLayout(self.newVisualLayout)
        self.RightLayout.addLayout(self.horizontalLayout_2)
        self.resetButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.resetButton.setObjectName("resetButton")
        self.resetButton.clicked.connect(self.reset_text)

        self.RightLayout.addWidget(self.resetButton)
        self.mainHorizontalLayout.addLayout(self.RightLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def reset_text(self):
        self.newQueryInput.clear()
        self.oldQueryInput.clear()

        self.newQEPOutput.clear()
        self.oldQEPOutput.clear()

    def getOldQueryInput(self):
        return self.oldQueryInput.toPlainText()
    def getNewQueryInput(self):
        return self.newQueryInput.toPlainText()

    def setSchema(self, schema=None):
        self.databaseSchema.reset()
        if schema is None:
            return
        for table in schema:
            table_item = QTreeWidgetItem([table])
            for attr in schema[table]:
                attr_item = QTreeWidgetItem([attr])
                table_item.addChild(attr_item)
            self.databaseSchema.addTopLevelItem(table_item)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.schemaLabel.setText(_translate("Form", "Database Schema"))
        self.oldQueryLabel.setText(_translate("Form", "Query Q"))
        self.oldQueryButton.setText(_translate("Form", "Submit Query"))
        self.oldQEPLabel.setText(_translate("Form", "QEP P"))
        self.oldVisualLabel.setText(_translate("Form", "Visual Plan P"))
        self.newQueryLabel.setText(_translate("Form", "Query Q\'"))
        self.newQueryButton.setText(_translate("Form", "Submit Update Query"))
        self.newQEPLabel.setText(_translate("Form", "QEP P\'"))
        self.newVisualLabel.setText(_translate("Form", "Visual Plan P\'"))
        self.resetButton.setText(_translate("Form", "Reset"))

