from PyQt5 import QtCore, QtGui, QtWidgets
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

        # Form.setObjectName("CZ4031-Group8-DSPProject2")
        # Form.resize(1920, 1080)
        self.mainHorizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.mainHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.mainHorizontalLayout.setObjectName("mainHorizontalLayout")
        self.LeftLayout = QtWidgets.QVBoxLayout()
        self.LeftLayout.setObjectName("LeftLayout")

        # -------------------------- DATABASE SCHEMA -----------------------------------------
        # Label
        self.schemaLabel = QtWidgets.QLabel(Form)
        self.schemaLabel.setObjectName("schemaLabel")
        self.LeftLayout.addWidget(self.schemaLabel)

        # QTreeWidget
        self.databaseSchema = QTreeWidget(Form)
        self.databaseSchema.setObjectName(u"databaseSchema")
        self.databaseSchema.setHeaderLabels(["Schema"])
        # self.databaseSchema.setStyleSheet("background-color: white;")

        # ----------------------- Instructions ------------------------------------------------
        self.instructions = QtWidgets.QTextBrowser(Form)
        # self.instructions.set
        self.instructions.setObjectName("instructions")
        self.instructions.setReadOnly(True)
        instructionsString = ("1. Once the Query Q has been submitted,  'Submit Query' button will be DISABLED. Click on the Reset button to re-enable it.\n\n2. Query Q' and 'Submit Updated Query' button will only be enabled when Query Q has been submitted.\n\n"
        "3. Creative Functionality: Improved user experience with Text-To-Speech capabilities to read your QEP for you! Press the 'Play' button under any of the QEP textboxes"
         "to play the audio that reads out the QEP to you, and press the 'Stop' button to stop the audio at any time.")

        self.instructions.setText(instructionsString)


        self.instructionsLabel = QtWidgets.QLabel(Form)
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
        self.oldQueryLabel = QtWidgets.QLabel(Form)
        self.oldQueryLabel.setObjectName("oldQueryLabel")
        self.OldQueryLayout.addWidget(self.oldQueryLabel)

        # Old Query Input
        self.oldQueryInput = QtWidgets.QTextBrowser(Form)
        # self.oldQueryInput.setFixedHeight(400)
        self.oldQueryInput.setObjectName("oldQueryInput")
        self.oldQueryInput.setReadOnly(False)
        self.OldQueryLayout.addWidget(self.oldQueryInput, 2)

        # Old Query Button
        self.oldQueryButton = QtWidgets.QPushButton(Form)
        self.oldQueryButton.setObjectName("oldQueryButton")

        self.OldQueryLayout.addWidget(self.oldQueryButton)
        self.TopLayout.addLayout(self.OldQueryLayout)

        self.oldQEPLayout = QtWidgets.QVBoxLayout()
        self.oldQEPLayout.setObjectName("oldQEPLayout")
        self.oldQEPLabel = QtWidgets.QLabel(Form)
        self.oldQEPLabel.setObjectName("oldQEPLabel")
        self.oldQEPLayout.addWidget(self.oldQEPLabel)


        # Display Old QEP Plan
        self.oldQEPOutput = QtWidgets.QTextBrowser(Form)
        self.oldQEPOutput.setObjectName("oldQEPOutput")

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

        self.oldQEPLayout.addWidget(self.oldQEPOutput)
        self.oldQEPLayout.addLayout(self.oldAudiohorizontalLayout)

        self.TopLayout.addLayout(self.oldQEPLayout)
        self.oldVisualLayout = QtWidgets.QVBoxLayout()
        self.oldVisualLayout.setObjectName("oldVisualLayout")
        self.oldVisualLabel = QtWidgets.QLabel(Form)
        self.oldVisualLabel.setObjectName("oldVisualLabel")
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
        self.newQEPLabel = QtWidgets.QLabel(Form)
        self.newQEPLabel.setObjectName("newQEPLabel")
        self.newQEPLayout.addWidget(self.newQEPLabel)

        # Display New QEP Plan
        self.diffBetweenQEPInput = QtWidgets.QTextBrowser(Form)
        self.diffBetweenQEPInput.setObjectName("diffBetweenQEPInput")

        self.newAudiohorizontalLayout = QtWidgets.QHBoxLayout()
        # self.horizontalLayout = QHBoxLayout()
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
        self.oldQEPOutput.clear()

    def getOldQueryInput(self):
        return self.oldQueryInput.toPlainText()
    def getNewQueryInput(self):
        return self.newQueryInput.toPlainText()

    def showOldQEP(self, text):
        self.oldQEPOutput.setText(text)
    def showNewQEP(self, text):
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
        # text output of passed qep
        # pgsql_qep_output = """
        #  -> Ending Steps
        # ['Gather  (cost=5366.32..39381.32 rows=150 width=266)', '  Workers Planned: 2']
        #      -> Hash Join
        # ['        Hash Cond: (o.o_custkey = c.c_custkey)']
        #            -> Seq Scan on orders o
        # []
        #            -> Hash
        # []
        #                  -> Seq Scan on customer c
        # ["                    Filter: ((c_name)::text ~~ '%cheng'::text)"]
        # """

        # pgsql_qep_output = """
        #  -> Finalize GroupAggregate
        # []
        #  -> Ending Steps
        # ['Finalize GroupAggregate  (cost=232260.49..232262.45 rows=6 width=236)', '  Group Key: l_returnflag, l_linestatus']
        #      -> Gather Merge
        # ['        Workers Planned: 2']
        #            -> Sort
        # ['              Sort Key: l_returnflag, l_linestatus']
        #                  -> Partial HashAggregate
        # ['                    Group Key: l_returnflag, l_linestatus']
        #                        -> Seq Scan on lineitem
        # ["                          Filter: (l_extendedprice > '100'::numeric)"]
        # """

        QEPtree1 = self.explainObj.build_QEP_tree(queryInput)
        visualPlan1 = self.explainObj.get_visual_plan(QEPtree1)

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


        # # Create a new graph
        first_value = output_dict[list(output_dict.keys())[0]]

        new_key = 'ROOT: ' + list(output_dict.keys())[0]
        new_dict = {new_key: first_value}

        del output_dict[list(output_dict.keys())[0]]

        new_dict.update(output_dict)

        output_dict = new_dict

        G = nx.DiGraph()
        #
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

        #
        # # # Draw the graph
        nx.draw(G, pos=pos, with_labels=True, node_shape="s",  node_color="none", bbox=dict(facecolor="#FFBF00", edgecolor='black', boxstyle='round,pad=1'))

        plt.margins(x=0.4, y=0.4)

        if type == "old":
            file_path = os.path.join(os.getcwd(), "oldVisualPlan" + str(".png"))
            if os.path.exists(file_path):
                os.remove(file_path)
            plt.savefig(file_path)
            pixmap = QtGui.QPixmap(file_path)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self.oldScene.addItem(item)
            self.oldGraphicsView.setScene(self.oldScene)
        else:
            file_path = os.path.join(os.getcwd(), "newVisualPlan" + str(".png"))
            if os.path.exists(file_path):
                os.remove(file_path)
            plt.savefig(file_path)
            pixmap = QtGui.QPixmap(file_path)
            item = QtWidgets.QGraphicsPixmapItem(pixmap)
            self.newScene.addItem(item)
            self.newGraphicsView.setScene(self.newScene)

    # Displays Pop up of Maximised QEP image
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
        self.oldQEPLabel.setText(_translate("Form", "Difference between SQL Queries"))
        self.oldVisualLabel.setText(_translate("Form", "Visual Plan P"))
        self.newQueryLabel.setText(_translate("Form", "Query Q\'"))
        self.newQueryButton.setText(_translate("Form", "Submit Updated Query"))
        self.newQEPLabel.setText(_translate("Form", "Difference between QEPs\'"))
        self.newVisualLabel.setText(_translate("Form", "Visual Plan P\'"))
        self.resetButton.setText(_translate("Form", "Reset"))


    def onClickedOldQueryButton(self):
        self.oldQueryButton.clicked.connect(self.analyseOldQuery)

        pgsql_qep_output = """
         -> Finalize GroupAggregate
        []
         -> Ending Steps
        ['Finalize GroupAggregate  (cost=122472.60..124116.88 rows=10028 width=248)', "  Group Key: n1.n_name, n2.n_name, (date_part('YEAR'::text, (lineitem.l_shipdate)::timestamp without time zone))"]
             -> Gather Merge
        ['        Workers Planned: 2']
                   -> Partial GroupAggregate
        ["              Group Key: n1.n_name, n2.n_name, (date_part('YEAR'::text, (lineitem.l_shipdate)::timestamp without time zone))"]
                         -> Sort
        ["                    Sort Key: n1.n_name, n2.n_name, (date_part('YEAR'::text, (lineitem.l_shipdate)::timestamp without time zone))"]
                               -> Hash Join
        ['                          Hash Cond: (lineitem.l_suppkey = supplier.s_suppkey)', "                          Join Filter: (((n1.n_name = 'FRANCE'::bpchar) AND (n2.n_name = 'GERMANY'::bpchar)) OR ((n1.n_name = 'GERMANY'::bpchar) AND (n2.n_name = 'FRANCE'::bpchar)))"]
                                     -> Nested Loop
        []
                                           -> Hash Join
        ['                                      Hash Cond: (orders.o_custkey = customer.c_custkey)']
                                                 -> Seq Scan on orders
        ["                                            Filter: (o_totalprice > '100'::numeric)"]
                                                 -> Hash
        []
                                                       -> Hash Join
        ['                                                  Hash Cond: (customer.c_nationkey = n2.n_nationkey)']
                                                             -> Seq Scan on customer
        ["                                                        Filter: (c_acctbal > '10'::numeric)"]
                                                             -> Hash
        []
                                                                   -> Seq Scan on nation n2
        ["                                                              Filter: ((n_name = 'GERMANY'::bpchar) OR (n_name = 'FRANCE'::bpchar))"]
                                           -> Index Scan using lineitem_pkey on lineitem
        ['                                      Index Cond: (l_orderkey = orders.o_orderkey)', "                                      Filter: ((l_shipdate >= '1995-01-01'::date) AND (l_shipdate <= '1996-12-31'::date))"]
                                     -> Hash
        []
                                           -> Hash Join
        ['                                      Hash Cond: (supplier.s_nationkey = n1.n_nationkey)']
                                                 -> Seq Scan on supplier
        []
                                                 -> Hash
        []
                                                       -> Seq Scan on nation n1
        ["                                                  Filter: ((n_name = 'FRANCE'::bpchar) OR (n_name = 'GERMANY'::bpchar))"]
        # """

        self.oldQueryButton.clicked.connect(lambda: self.generateQEP("old",self.getOldQueryInput()))
    def onClickedNewQueryButton(self):

        pgsql_qep_output = """
         -> Ending Steps
        ['Gather  (cost=5366.32..39381.32 rows=150 width=266)', '  Workers Planned: 2']
             -> Hash Join
        ['        Hash Cond: (o.o_custkey = c.c_custkey)']
                   -> Seq Scan on orders o
        []
                   -> Hash
        []
                         -> Seq Scan on customer c
        ["                    Filter: ((c_name)::text ~~ '%cheng'::text)"]
        """






        self.newQueryButton.clicked.connect(self.analyseNewQuery)
        self.newQueryButton.clicked.connect(lambda: self.generateQEP("new",self.getNewQueryInput()))
        self.showNewVisualPlanFullBtn.clicked.connect(lambda: self.showNewVisualPlanFullBtn.setEnabled(True))

    def onClickedResetButton(self):
        self.resetButton.clicked.connect(lambda: self.oldQueryButton.setEnabled(True))
        self.resetButton.clicked.connect(lambda: self.oldQueryInput.setReadOnly(False))
        self.resetButton.clicked.connect(lambda: self.newQueryButton.setEnabled(False))
        self.resetButton.clicked.connect(lambda: self.newQueryInput.setReadOnly(True))

        self.resetButton.clicked.connect(lambda: self.playOldButton.setEnabled(False))
        self.resetButton.clicked.connect(lambda: self.stopOldButton.setEnabled(False))
        self.resetButton.clicked.connect(lambda: self.playNewButton.setEnabled(False))
        self.resetButton.clicked.connect(lambda: self.stopNewButton.setEnabled(False))

        self.resetButton.clicked.connect(self.removeGraphicsViews)

        self.resetButton.clicked.connect(lambda: self.showOldVisualPlanFullBtn.setEnabled(False))
        self.resetButton.clicked.connect(lambda: self.showNewVisualPlanFullBtn.setEnabled(False))

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
            self.showOldQEP(query.strip())
            self.textToSpeech(self.oldQEPOutput.toPlainText(), "oldQuery")

            self.showOldVisualPlanFullBtn.setEnabled(True)

            self.disabledStateForOldQuery()
            self.newQueryButton.setEnabled(True)
            self.newQueryInput.setReadOnly(False)
        else:
            self.showError("Please input Query Q")

    def analyseNewQuery(self):
        query = self.getNewQueryInput()
        if query.strip() != "":

            # EXPLAIN FOR QEP
            QEPtree1 = self.explainObj.build_QEP_tree(self.getOldQueryInput())
            QEPtree2 = self.explainObj.build_QEP_tree(self.getNewQueryInput())
            print(self.getOldQueryInput())
            # Get explanation for specified query (q1 or q2) by passing in
            # the root node of the respective QEP tree
            # Returns List[str] of explanations
            explanationQEP1 = self.explainObj.get_QEP_explanation(QEPtree1)
            explanationQEP2 = self.explainObj.get_QEP_explanation(QEPtree2)
            # Get the comparisons between 2 QEP
            # by passing the 2 QEPtrees as params
            # Returns List[str] of comparisons between the 2 QEPs
            comparison = self.explainObj.get_QEP_comparison(QEPtree1, QEPtree2)

            differenceExplanationInQEP = ["  Explanation QEP 1  "] + explanationQEP1 + ["  Explanation QEP 2  "] + explanationQEP2 + ["  Comparison  "] + comparison

            concatDiff = ""
            for diff in differenceExplanationInQEP:
                concatDiff = concatDiff + diff + '\n\n'

            self.showNewQEP(concatDiff)
            self.textToSpeech(self.diffBetweenQEPInput.toPlainText(), "newQuery")

            # differences = self.explainObj.compare_sql(self.getOldQueryInput(), self.getNewQueryInput())
            # explaination = self.explainObj.explainSQL(differences)
            # self.explainObj.printSQLexplain(differences, explaination)
            #
            # self.showOldQEP(differences)
            # self.textToSpeech(self.diffBetweenQEPInput.toPlainText(), "newQuery")

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


