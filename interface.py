from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore


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
        # self.databaseSchema.setStyleSheet("background-color: white;")

        # ----------------------- Instructions ------------------------------------------------
        self.instructions = QtWidgets.QTextBrowser(self.horizontalLayoutWidget_2)
        self.instructions.setObjectName("instructions")
        self.instructions.setReadOnly(True)
        instructionsString = ("1. Once the Query Q has been submitted,  'Submit Query' button will be DISABLED. Click on the Reset button to re-enable it.\n\n2. Query Q' and 'Submit Updated Query' button will only be enabled when Query Q has been submitted.\n\n"
        "3. Creative Functionality: Improved user experience with Text-To-Speech capabilities to read your QEP for you! Press the 'Play' button under any of the QEP textboxes"
         "to play the audio that reads out the QEP to you, and press the 'Stop' button to stop the audio at any time.")

        self.instructions.setText(instructionsString)

        self.instructionsLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.instructionsLabel.setObjectName("instructionsLabel")
        self.instructionsLabel.setText("INSTRUCTIONS FOR USE")



        self.LeftLayout.addWidget(self.databaseSchema)
        self.LeftLayout.addWidget(self.instructionsLabel)
        self.LeftLayout.addWidget(self.instructions)

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

        self.oldAudiohorizontalLayout = QtWidgets.QHBoxLayout()
        # self.horizontalLayout = QHBoxLayout()
        self.oldAudiohorizontalLayout.setObjectName(u"horizontalLayout")

        # Play button
        self.playOldButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.playOldButton.setObjectName("playOldButton")
        self.playOldButton.setText("Play \U0001F50A")
        self.playOldButton.setEnabled(False)
        self.oldAudiohorizontalLayout.addWidget(self.playOldButton)


        # Stop button
        self.stopOldButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.stopOldButton.setObjectName("stopOldButton")
        self.stopOldButton.setText("Stop \U0001F507")
        self.stopOldButton.setEnabled(False)
        self.oldAudiohorizontalLayout.addWidget(self.stopOldButton)
        # self.horizontalLayoutWidget_2.addWidget(self.horizontalLayout)

        self.oldQEPLayout.addWidget(self.oldQEPOutput)
        self.oldQEPLayout.addLayout(self.oldAudiohorizontalLayout)
        # self.oldQEPLayout.addWidget(self.playOldButton)
        # self.oldQEPLayout.addWidget(self.stopOldButton)

        self.TopLayout.addLayout(self.oldQEPLayout)
        self.oldVisualLayout = QtWidgets.QVBoxLayout()
        self.oldVisualLayout.setObjectName("oldVisualLayout")
        self.oldVisualLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.oldVisualLabel.setObjectName("oldVisualLabel")
        self.oldVisualLayout.addWidget(self.oldVisualLabel)

        # Display Old Visual Plan
        self.oldGraphicsView = QtWidgets.QGraphicsView(self.horizontalLayoutWidget_2)
        self.oldGraphicsView.setObjectName("oldGraphicsView")
        # self.oldGraphicsView.setStyleSheet("background-color: white;")
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
        self.newQueryInput.setReadOnly(True)

        self.NewQueryLayout.addWidget(self.newQueryInput)


        # New Query Button
        self.newQueryButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.newQueryButton.setObjectName("newQueryButton")
        self.newQueryButton.setEnabled(False)

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

        self.newAudiohorizontalLayout = QtWidgets.QHBoxLayout()
        # self.horizontalLayout = QHBoxLayout()
        self.newAudiohorizontalLayout.setObjectName(u"newhorizontalLayout")

        # Play button
        self.playNewButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.playNewButton.setObjectName("playOldButton")
        self.playNewButton.setText("Play \U0001F50A")
        self.playNewButton.setEnabled(False)
        self.newAudiohorizontalLayout.addWidget(self.playNewButton)

        # Stop button
        self.stopNewButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.stopNewButton.setObjectName("stopOldButton")
        self.stopNewButton.setText("Stop \U0001F507")
        self.stopNewButton.setEnabled(False)
        self.newAudiohorizontalLayout.addWidget(self.stopNewButton)

        self.newQEPLayout.addWidget(self.newQEPOutput)
        self.newQEPLayout.addLayout(self.newAudiohorizontalLayout)
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



    def showOldQEP(self, text):
        self.oldQEPOutput.setText(text)
    def showNewQEP(self, text):
        self.newQEPOutput.setText(text)

    def showError(self, errMessage, execption=None):
        dialog = QMessageBox()
        dialog.setStyleSheet("QLabel{min-width: 300px;}");
        dialog.setWindowTitle("Error")
        dialog.setText(errMessage)
        if execption is not None:
            dialog.setDetailedText(str(execption))
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.exec_()

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
        self.newQueryButton.setText(_translate("Form", "Submit Updated Query"))
        self.newQEPLabel.setText(_translate("Form", "QEP P\'"))
        self.newVisualLabel.setText(_translate("Form", "Visual Plan P\'"))
        self.resetButton.setText(_translate("Form", "Reset"))

