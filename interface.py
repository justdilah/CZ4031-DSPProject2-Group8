from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QUrl,QSize, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from gtts import gTTS
import os

import networkx as nx
import matplotlib.pyplot as plt

class Ui_Form(object):
    def setupUi(self, Form, explainObj):
        self.explainObj = explainObj
        if Form.objectName():
            Form.setObjectName(u"CZ4031-Group8-DSPProject2")
        Form.resize(1167, 794)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")

        self.form = Form

        self.mainHorizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.mainHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.mainHorizontalLayout.setObjectName("mainHorizontalLayout")
        self.LeftLayout = QtWidgets.QVBoxLayout()
        self.LeftLayout.setObjectName("LeftLayout")

        # -------------------------- DATABASE SCHEMA -----------------------------------------
        # Label
        self.schemaLabel = QtWidgets.QLabel(Form)
        self.schemaLabel.setObjectName("schemaLabel")
        # self.schemaLabel.setFont(QtGui.QFont("Times", 50, QtGui.QFont.Bold))
        self.schemaLabel.setStyleSheet("font: 8pt")
        self.LeftLayout.addWidget(self.schemaLabel)

        # QTreeWidget
        self.databaseSchema = QTreeWidget(Form)
        self.databaseSchema.setObjectName(u"databaseSchema")
        self.databaseSchema.setHeaderLabels(["Schema"])
        self.databaseSchema.setStyleSheet("font: 8pt")

        # ----------------------- Instructions ------------------------------------------------
        self.instructions = QtWidgets.QTextBrowser(Form)
        self.instructions.setObjectName("instructions")
        self.instructions.setReadOnly(True)
        self.instructions.setFontPointSize(9)

        instructionsString = (
            "1. Once the Query Q has been submitted, 'Submit Query' button will be DISABLED. Click on the Reset button to re-enable it.\n\n"
            "2. Query Q' and 'Submit Updated Query' button will only be enabled when Query Q has been submitted.\n\n"
            "3. Visual Plans will be available for viewing after submission of queries.\n\n"
            "4. Difference between SQLs and QEPs will require both Query Q and Q' to be submitted.\n\n"
            "5. Creative Functionality: Improved user experience with Text-To-Speech capabilities to read the difference explanations for you! "
            "Press the 'Play' button under any of the QEP textboxes"
            " to play the audio that reads out the explanations to you, and press the 'Stop' button to stop the audio at any time.")
        self.instructions.setText(instructionsString)

        # Label
        self.instructionsLabel = QtWidgets.QLabel(Form)
        self.instructionsLabel.setObjectName("instructionsLabel")
        self.instructionsLabel.setText("INSTRUCTIONS FOR USE")
        self.instructionsLabel.setStyleSheet("font: 8pt")

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
        self.oldQueryLabel = QtWidgets.QLabel(Form)
        self.oldQueryLabel.setObjectName("oldQueryLabel")
        self.oldQueryLabel.setStyleSheet("font: 8pt")
        self.OldQueryLayout.addWidget(self.oldQueryLabel)

        # Old Query Input
        self.oldQueryInput = QtWidgets.QTextBrowser(Form)
        # self.oldQueryInput.setFixedHeight(400)
        self.oldQueryInput.setObjectName("oldQueryInput")
        self.oldQueryInput.setReadOnly(False)
        self.oldQueryInput.setFontPointSize(9)
        self.OldQueryLayout.addWidget(self.oldQueryInput, 2)

        # Old Query Button
        self.oldQueryButton = QtWidgets.QPushButton(Form)
        self.oldQueryButton.setObjectName("oldQueryButton")

        self.OldQueryLayout.addWidget(self.oldQueryButton)
        self.TopLayout.addLayout(self.OldQueryLayout)

        self.oldQEPLayout = QtWidgets.QVBoxLayout()
        self.oldQEPLayout.setObjectName("oldQEPLayout")
        self.diffBetweenSQLLabel = QtWidgets.QLabel(Form)
        self.diffBetweenSQLLabel.setObjectName("diffBetweenSQLLabel")
        self.diffBetweenSQLLabel.setStyleSheet("font: 8pt")
        self.oldQEPLayout.addWidget(self.diffBetweenSQLLabel)

        # ======================================== Differences between 2 SQL Inputs ===========================
        # Display differences between the 2 SQL Queries
        self.diffBetweenSQLInput = QtWidgets.QTextBrowser(Form)
        self.diffBetweenSQLInput.setObjectName("diffBetweenSQLInput")
        self.diffBetweenSQLInput.setFontPointSize(9)

        self.oldAudiohorizontalLayout = QtWidgets.QHBoxLayout()
        self.oldAudiohorizontalLayout.setObjectName(u"horizontalLayout")

        # Play button
        self.playOldButton = QtWidgets.QPushButton(Form)
        self.playOldButton.setObjectName("playOldButton")
        self.playOldButton.setText("Play \U0001F50A")
        self.playOldButton.setEnabled(False)
        self.oldAudiohorizontalLayout.addWidget(self.playOldButton)


        # Stop button
        self.stopOldButton = QtWidgets.QPushButton(Form)
        self.stopOldButton.setObjectName("stopOldButton")
        self.stopOldButton.setText("Stop \U0001F507")
        self.stopOldButton.setEnabled(False)
        self.oldAudiohorizontalLayout.addWidget(self.stopOldButton)
        # Form.addWidget(self.horizontalLayout)

        self.oldQEPLayout.addWidget(self.diffBetweenSQLInput)
        self.oldQEPLayout.addLayout(self.oldAudiohorizontalLayout)

        self.TopLayout.addLayout(self.oldQEPLayout)
        self.oldVisualLayout = QtWidgets.QVBoxLayout()
        self.oldVisualLayout.setObjectName("oldVisualLayout")
        self.oldVisualLabel = QtWidgets.QLabel(Form)
        self.oldVisualLabel.setObjectName("oldVisualLabel")
        self.oldVisualLabel.setStyleSheet("font: 8pt")
        self.oldVisualLayout.addWidget(self.oldVisualLabel)

        # Display Old Visual Plan
        self.oldGraphicsView = QtWidgets.QGraphicsView(Form)
        self.oldGraphicsView.setObjectName("oldGraphicsView")
        self.oldScene = QtWidgets.QGraphicsScene(Form)
        self.oldVisualLayout.addWidget(self.oldGraphicsView)

        self.showOldVisualPlanFullBtn = QtWidgets.QPushButton(Form)
        self.showOldVisualPlanFullBtn.setObjectName("showFullOld")
        self.showOldVisualPlanFullBtn.setText("Maximimise Visual Plan P")
        self.showOldVisualPlanFullBtn.setEnabled(False)

        self.oldVisualLayout.addWidget(self.showOldVisualPlanFullBtn)

        self.TopLayout.addLayout(self.oldVisualLayout)
        self.RightLayout.addLayout(self.TopLayout)
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomLayout.setObjectName("bottomLayout")

        # -------------------------- NEW QUERY -----------------------------------------
        self.NewQueryLayout = QtWidgets.QVBoxLayout()
        self.NewQueryLayout.setObjectName("NewQueryLayout")

        # Label
        self.newQueryLabel = QtWidgets.QLabel(Form)
        self.newQueryLabel.setObjectName("newQueryLabel")
        self.newQueryLabel.setStyleSheet("font: 8pt")
        self.NewQueryLayout.addWidget(self.newQueryLabel)

        # New Query Input
        self.newQueryInput = QtWidgets.QTextBrowser(Form)
        # self.newQueryInput.setFixedHeight(400)
        self.newQueryInput.setObjectName("newQueryInput")
        self.newQueryInput.setReadOnly(True)

        self.NewQueryLayout.addWidget(self.newQueryInput)


        # New Query Button
        self.newQueryButton = QtWidgets.QPushButton(Form)
        self.newQueryButton.setObjectName("newQueryButton")
        self.newQueryButton.setEnabled(False)

        self.NewQueryLayout.addWidget(self.newQueryButton)
        self.bottomLayout.addLayout(self.NewQueryLayout)
        self.newQEPLayout = QtWidgets.QVBoxLayout()
        self.newQEPLayout.setObjectName("newQEPLayout")
        self.diffBetweenQEPLabel = QtWidgets.QLabel(Form)
        self.diffBetweenQEPLabel.setObjectName("diffBetweenQEPLabel")
        self.diffBetweenQEPLabel.setStyleSheet("font: 8pt")
        self.newQEPLayout.addWidget(self.diffBetweenQEPLabel)

        # ======================================== Differences between 2 QEP plans ===========================
        # Display differences between 2 QEP plans
        self.diffBetweenQEPInput = QtWidgets.QTextBrowser(Form)
        self.diffBetweenQEPInput.setObjectName("diffBetweenQEPInput")
        self.diffBetweenQEPInput.setFontPointSize(9)

        self.newAudiohorizontalLayout = QtWidgets.QHBoxLayout()
        self.newAudiohorizontalLayout.setObjectName(u"newhorizontalLayout")

        # Play button
        self.playNewButton = QtWidgets.QPushButton(Form)
        self.playNewButton.setObjectName("playOldButton")
        self.playNewButton.setText("Play \U0001F50A")
        self.playNewButton.setEnabled(False)
        self.newAudiohorizontalLayout.addWidget(self.playNewButton)

        # Stop button
        self.stopNewButton = QtWidgets.QPushButton(Form)
        self.stopNewButton.setObjectName("stopOldButton")
        self.stopNewButton.setText("Stop \U0001F507")
        self.stopNewButton.setEnabled(False)
        self.newAudiohorizontalLayout.addWidget(self.stopNewButton)

        self.newQEPLayout.addWidget(self.diffBetweenQEPInput)
        self.newQEPLayout.addLayout(self.newAudiohorizontalLayout)
        self.bottomLayout.addLayout(self.newQEPLayout)
        self.newVisualLayout = QtWidgets.QVBoxLayout()
        self.newVisualLayout.setObjectName("newVisualLayout")
        self.newVisualLabel = QtWidgets.QLabel(Form)
        self.newVisualLabel.setObjectName("newVisualLabel")
        self.newVisualLabel.setStyleSheet("font: 8pt")
        self.newVisualLayout.addWidget(self.newVisualLabel)

        # Display New Visual Plan
        self.newGraphicsView = QtWidgets.QGraphicsView(Form)
        self.newGraphicsView.setObjectName("newGraphicsView")
        self.newScene = QtWidgets.QGraphicsScene(Form)

        self.newVisualLayout.addWidget(self.newGraphicsView)

        # Maximise Button
        self.showNewVisualPlanFullBtn = QtWidgets.QPushButton(Form)
        self.showNewVisualPlanFullBtn.setObjectName("showFullNew")
        self.showNewVisualPlanFullBtn.setText("Maximimise Visual Plan P'")
        self.showNewVisualPlanFullBtn.setEnabled(False)

        self.newVisualLayout.addWidget(self.showNewVisualPlanFullBtn)

        self.bottomLayout.addLayout(self.newVisualLayout)
        self.RightLayout.addLayout(self.bottomLayout)
        self.resetButton = QtWidgets.QPushButton(Form)
        self.resetButton.setObjectName("resetButton")
        self.resetButton.clicked.connect(self.reset_text)

        self.RightLayout.addWidget(self.resetButton)

        self.TopLayout.setStretch(0, 2)
        self.TopLayout.setStretch(1, 2)
        self.TopLayout.setStretch(2, 2)

        self.bottomLayout.setStretch(0, 2)
        self.bottomLayout.setStretch(1, 2)
        self.bottomLayout.setStretch(2, 2)

        self.RightLayout.setStretch(0, 3)
        self.RightLayout.setStretch(1, 3)
        self.RightLayout.setStretch(2, 1)

        self.mainHorizontalLayout.addLayout(self.RightLayout)

        self.mainHorizontalLayout.setStretch(0, 2)
        self.mainHorizontalLayout.setStretch(1, 4)

        self.gridLayout.addLayout(self.mainHorizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        #---------------- Button Clicks -----------------------------
        # On CLicked Methods for Submit Buttons
        self.onClickedOldQueryButton()
        self.onClickedNewQueryButton()

        # Reset Button
        self.onClickedResetButton()

        # Text-to-speech capabilities
        self.player = QMediaPlayer()

        self.onClickedOldPlayButton()
        self.onClickedOldStopButton()

        self.onClickedNewPlayButton()
        self.onClickedNewStopButton()

        self.onClickedMaxImageButton()

    def reset_text(self):
        self.newQueryInput.clear()
        self.oldQueryInput.clear()

        self.diffBetweenQEPInput.clear()
        self.diffBetweenSQLInput.clear()

    def getOldQueryInput(self):
        return self.oldQueryInput.toPlainText()
    def getNewQueryInput(self):
        return self.newQueryInput.toPlainText()

    def showDiffBetweenSQL(self, text):
        self.diffBetweenSQLInput.setText(text)
    def showDiffBetweenQEP(self, text):
        self.diffBetweenQEPInput.setText(text)

    # Displays error message
    def showError(self, errMessage, execption=None):
        dialog = QMessageBox()
        dialog.setStyleSheet("QLabel{min-width: 300px;}");
        dialog.setWindowTitle("Error")
        dialog.setText(errMessage)
        if execption is not None:
            dialog.setDetailedText(str(execption))
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.exec_()

    # Generates QEP image to be displayed
    def generateQEP(self,type,queryInput):

        QEPtree_temp = self.explainObj.build_QEP_tree(queryInput)
        visualPlan1 = self.explainObj.get_visual_plan(QEPtree_temp)
        if visualPlan1:
            pass
        else:
            self.showError("An error occurred:" + "\n\nPlease input a valid query.\nThe application will now rollback the transaction.")
            self.explainObj.rollback()
            self.reset()
            return

        qep_output = ""
        for vs1Item in visualPlan1:
            qep_output = qep_output + vs1Item + '\n'

        # take only text which has "->" which indicates the nodes except "-> Ending Steps"
        strArray = qep_output.strip().split("\n")
        strArray = [x for x in strArray if "[" not in x]
        qep_output = [x for x in strArray if "Ending" not in x]

        # Initialize an empty dictionary to hold the output
        output_dict = {}
        #
        # # Iterate over each element in the input list
        for i, item in enumerate(qep_output):

            # Count the number of indentations
            num_indentations = len(item) - len(item.lstrip(' '))

            # Get the label for the current item
            label = item.strip().lstrip('-> ')

            # Initialize an empty list to hold the children of the current item
            children = []

            for j in range(i + 1, len(qep_output)):
                next_indentations = len(qep_output[j]) - len(qep_output[j].lstrip(' '))
                # print(qep_output[j] + " - " + str(next_indentations) + " " + str(num_indentations))
                if next_indentations > num_indentations:
                    if children:
                        prev_indentations = len(qep_output[j - 1]) - len(qep_output[j - 1].lstrip(' '))
                        if prev_indentations == next_indentations:
                            children.append(qep_output[j].strip().lstrip('-> '))
                        else:
                            break
                    else:
                        children.append(qep_output[j].strip().lstrip('-> '))
                else:
                    break
            output_dict[label] = children


        # Create a new graph
        first_value = output_dict[list(output_dict.keys())[0]]

        new_key = 'ROOT: ' + list(output_dict.keys())[0]
        new_dict = {new_key: first_value}

        del output_dict[list(output_dict.keys())[0]]

        new_dict.update(output_dict)

        output_dict = new_dict

        G = nx.DiGraph()
        # # Add nodes to the graph in left deep order
        def add_node_and_children(node):
            if node in G:
                return
            G.add_node(node)
            for child in output_dict[node]:
                # if 'Workers Planned' not in child:
                add_node_and_children(child)
                G.add_edge(node, child)

        add_node_and_children(list(output_dict.keys())[0])

        # Set layout
        if G.number_of_nodes() <= 5:
            pos = nx.kamada_kawai_layout(G)
            fig, ax = plt.subplots(figsize=(25, 5))
        else:
            pos = nx.circular_layout(G)
            fig, ax = plt.subplots(figsize=(25, 10))


        # Draw the graph
        nx.draw(G, pos=pos, with_labels=True, node_shape="s",  node_color="none", bbox=dict(facecolor="#FFBF00", edgecolor='black', boxstyle='round,pad=1'))

        plt.margins(x=0.4, y=0.4)

        if type == "old":
            file_path = os.path.join(os.getcwd(), "oldVisualPlan" + str(".png"))
            if os.path.exists(file_path):
                os.remove(file_path)
            # Generate PNG file of the graph
            plt.savefig(file_path)
            # Display Visual Plan for Old Query
            pixmap = QtGui.QPixmap(file_path)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self.oldScene.addItem(item)
            self.oldGraphicsView.setScene(self.oldScene)
        else:

            file_path = os.path.join(os.getcwd(), "newVisualPlan" + str(".png"))
            if os.path.exists(file_path):
                os.remove(file_path)
            # Generate PNG file of the graph
            plt.savefig(file_path)
            # Display Visual Plan for New Query
            pixmap = QtGui.QPixmap(file_path)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self.newScene.addItem(item)
            self.newGraphicsView.setScene(self.newScene)


    # Displays Pop up of Maximised Visual Plan image
    def showMaxImage(self, type):
        dialog = QDialog()
        dialog.setStyleSheet("QLabel{min-width: 300px;}");

        dialog.newGraphicsView = QtWidgets.QGraphicsView()
        if type == "old":
            file_path = os.path.join(os.getcwd(), "oldVisualPlan" + str(".png"))
            dialog.setWindowTitle("Visual Plan P")

            pixmap = QtGui.QPixmap(file_path)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self.oldScene.addItem(item)
            dialog.newGraphicsView.setScene(self.oldScene)

        else:
            file_path = os.path.join(os.getcwd(), "newVisualPlan" + str(".png"))
            dialog.setWindowTitle("Visual Plan P'")
            pixmap = QtGui.QPixmap(file_path)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self.newScene.addItem(item)
            dialog.newGraphicsView.setScene(self.newScene)

        lay = QVBoxLayout(dialog)
        dialog.setLayout(lay)
        lay.addWidget(dialog.newGraphicsView)
        dialog.exec_()

    def setSchema(self):
        self.databaseSchema.reset()
        schema = self.explainObj.updateSchema()

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
        self.diffBetweenSQLLabel.setText(_translate("Form", "Difference between SQL Queries"))
        self.oldVisualLabel.setText(_translate("Form", "Visual Plan P"))
        self.newQueryLabel.setText(_translate("Form", "Query Q\'"))
        self.newQueryButton.setText(_translate("Form", "Submit Updated Query"))
        self.diffBetweenQEPLabel.setText(_translate("Form", "Difference between QEPs\'"))
        self.newVisualLabel.setText(_translate("Form", "Visual Plan P\'"))
        self.resetButton.setText(_translate("Form", "Reset"))

    def onClickedOldQueryButton(self):
        self.oldQueryButton.clicked.connect(self.analyseOldQuery)
        # self.oldQueryButton.clicked.connect(lambda: self.generateQEP("old",self.getOldQueryInput()))

    def generatingPopUp(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Difference Explanations Generating...")
        msg.setText(
            "<p style='font-size: 16px;'>It will take some time to generate the Explanation for differences, press the 'Ok' button <b>NOW</b> and please wait.</p>")
        x = msg.exec_()

    def onClickedNewQueryButton(self):
        self.newQueryButton.clicked.connect(self.analyseNewQuery)


    def onClickedResetButton(self):
        self.resetButton.clicked.connect(self.reset)

    def reset(self):
        self.oldQueryButton.setEnabled(True)
        self.oldQueryInput.setReadOnly(False)
        self.oldQueryInput.clear()
        self.newQueryButton.setEnabled(False)
        self.newQueryInput.setReadOnly(True)
        self.newQueryInput.clear()

        self.playOldButton.setEnabled(False)
        self.stopOldButton.setEnabled(False)
        self.playNewButton.setEnabled(False)
        self.stopNewButton.setEnabled(False)

        self.removeGraphicsViews()

        self.showOldVisualPlanFullBtn.setEnabled(False)
        self.showNewVisualPlanFullBtn.setEnabled(False)
    def removeGraphicsViews(self):
        self.oldGraphicsView.deleteLater()
        self.oldGraphicsView = QtWidgets.QGraphicsView(self.form)
        self.oldVisualLayout.insertWidget(1, self.oldGraphicsView)

        self.newGraphicsView.deleteLater()
        self.newGraphicsView = QtWidgets.QGraphicsView(self.form)
        self.newVisualLayout.insertWidget(1, self.newGraphicsView)
    def onClickedMaxImageButton(self):
        self.showOldVisualPlanFullBtn.clicked.connect(lambda: self.showMaxImage("old"))
        self.showNewVisualPlanFullBtn.clicked.connect(lambda: self.showMaxImage("new"))


    def disabledStateForOldQuery(self):
        self.oldQueryButton.setEnabled(False)
        self.oldQueryInput.setReadOnly(True)

    def analyseOldQuery(self):
        query = self.getOldQueryInput()
        if query.strip() != "":
            self.showOldVisualPlanFullBtn.setEnabled(True)

            self.disabledStateForOldQuery()
            self.newQueryButton.setEnabled(True)
            self.newQueryInput.setReadOnly(False)
            self.generateQEP("old", self.getOldQueryInput())
        else:
            self.showError("Please input Query Q")

    def analyseNewQuery(self):
        query = self.getNewQueryInput()
        if query.strip() != "":

            # EXPLAIN FOR QEP
            QEPtree1 = self.explainObj.build_QEP_tree(self.getNewQueryInput())

            if QEPtree1 is None:
                self.showError("An error occurred:" + "\n\nPlease input a valid query.\nThe application will now rollback the transaction.")
                self.explainObj.rollback()
                self.reset()
                return

            # POP UP TO INFORM USER THAT IT WILL TAKE A BIT OF TIME TO GENERATE QEP
            self.generatingPopUp()

            # GENERATE QEP PLAN FOR NEW QUERY INPUT
            self.generateQEP("new", self.getNewQueryInput())

            QEPtree2 = self.explainObj.build_QEP_tree(self.getNewQueryInput())
            # Get explanation for specified query (q1 or q2) by passing in
            # the root node of the respective QEP tree
            # Returns List[str] of explanations
            explanationQEP1 = self.explainObj.get_QEP_explanation(QEPtree1)
            explanationQEP2 = self.explainObj.get_QEP_explanation(QEPtree2)
            # Get the comparisons between 2 QEP
            # by passing the 2 QEPtrees as params
            # Returns List[str] of comparisons between the 2 QEPs
            comparison = self.explainObj.get_QEP_comparison(QEPtree1, QEPtree2)

            differenceExplanationInQEP = ["  <b>Explanation QEP 1</b>  "] + explanationQEP1 + ["  <b>Explanation QEP 2</b>  "] + explanationQEP2 + ["  <b>Comparison</b>  "] + comparison

            concatDiff = '<p style="font-size: 18px;">'
            for diff in differenceExplanationInQEP:
                concatDiff = concatDiff + diff + '</b><br><br>'
            concatDiff = concatDiff + "</p>"
            self.showDiffBetweenQEP(concatDiff)
            self.textToSpeech(self.diffBetweenQEPInput.toPlainText(), "newQuery")
            differences = self.explainObj.compare_sql(self.getOldQueryInput(), self.getNewQueryInput())
            explaination = self.explainObj.explainSQL(differences)

            concatDiffSQL = self.explainObj.concatDifferencesExplainSQL(differences, explaination)


            self.showDiffBetweenSQL(concatDiffSQL)
            self.textToSpeech(self.diffBetweenSQLInput.toPlainText(), "oldQuery")

            self.showNewVisualPlanFullBtn.setEnabled(True)
            self.stopNewButton.setEnabled(True)
            self.playNewButton.setEnabled(True)
            self.stopOldButton.setEnabled(True)
            self.playOldButton.setEnabled(True)

        else:
            self.showError("Please input Query Q'")


    # ----------------------------------- Text-to-Speech -----------------------------------------------------
    def onClickedOldPlayButton(self):
        self.playOldButton.clicked.connect(lambda: self.playAudioFile("oldQuery"))

    def onClickedOldStopButton(self):
        self.stopOldButton.clicked.connect(self.stopAudioFile)

    def onClickedNewPlayButton(self):
        self.playNewButton.clicked.connect(lambda: self.playAudioFile("newQuery"))

    def onClickedNewStopButton(self):
        self.stopNewButton.clicked.connect(self.stopAudioFile)

    def textToSpeech(self, text, typeOfQuery):
        speaker = gTTS(text=text, lang="en", slow=False)

        file_path = os.path.join(os.getcwd(), typeOfQuery + str(".mp3"))
        if os.path.exists(file_path):
            os.remove(file_path)

        # saves the text speech as an MP3
        speaker.save(typeOfQuery + str(".mp3"))

        # returns stat_result object
        statbuf = os.stat(typeOfQuery + str(".mp3"))

        # statbuf.st_size -> represents the size of the file in kbytes -> convert to MBytes
        mbytes = statbuf.st_size / 1024

        # MB / 200 MBPS -> to get the duration of the mp3 in seconds
        duration = mbytes / 200

    def stopAudioFile(self):
        self.player.pause()

    def playAudioFile(self, typeOfQuery):
        mp3_name = typeOfQuery + str(".mp3")
        file_path = os.path.join(os.getcwd(), mp3_name)
        url = QUrl.fromLocalFile(file_path)

        content = QMediaContent(url)
        self.player.setMedia(QMediaContent())  # reset the media player
        self.player.setMedia(content)
        self.player.play()


