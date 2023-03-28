from project import DatabaseCursor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import json

FILE_CONFIG = "config.json"


class Explain:
    def __init__(self, ui):
        # Define configuration file
        with open(FILE_CONFIG, "r") as file:
            config = json.load(file)
            print(config)
            self.config = config["TPC-H"]

        # Initialise UI
        self.interface = ui

        # Retrieve and display database schema
        self.onDatabaseChanged()

        # On CLicked Methods for Submit Buttons
        self.onClickedOldQueryButton()
        self.onClickedNewQueryButton()

        # Reset Button
        self.onClickedResetButton()

    def onDatabaseChanged(self):
        self.updateSchema()

    def checkConfigFileExists(self):
        if not hasattr(self, "config") or self.config == None:
            return False

        return True

    def onClickedOldQueryButton(self):
        self.interface.oldQueryButton.clicked.connect(self.analyseOldQuery)
    def onClickedNewQueryButton(self):
        self.interface.newQueryButton.clicked.connect(self.analyseNewQuery)
    def onClickedResetButton(self):
        self.interface.resetButton.clicked.connect(lambda: self.interface.oldQueryButton.setEnabled(True))
        self.interface.resetButton.clicked.connect(lambda: self.interface.oldQueryInput.setReadOnly(False))
        self.interface.resetButton.clicked.connect(lambda: self.interface.newQueryButton.setEnabled(False))
        self.interface.resetButton.clicked.connect(lambda: self.interface.newQueryInput.setReadOnly(True))

    def disabledStateForOldQuery(self):
        self.interface.oldQueryButton.setEnabled(False)
        self.interface.oldQueryInput.setReadOnly(True)

    def analyseOldQuery(self):
        query = self.interface.getOldQueryInput()
        if query.strip() != "":
            self.interface.showOldQEP(query.strip())
            self.disabledStateForOldQuery()
            self.interface.newQueryButton.setEnabled(True)
            self.interface.newQueryInput.setReadOnly(False)
        else:
            self.interface.showError("Please input Query Q")

    def analyseNewQuery(self):
        query = self.interface.getNewQueryInput()
        if query.strip() != "":
            self.interface.showNewQEP(query.strip())
        else:
            self.interface.showError("Please input Query Q'")



    def updateSchema(self):
        if not self.checkConfigFileExists():
            self.interface.setSchema(None)
            print("Configuration file does not exists")
            return

        try:
            with DatabaseCursor(self.config) as cursor:

                query = "SELECT table_name, column_name, data_type, character_maximum_length as length FROM information_schema.columns WHERE table_schema='public' ORDER BY table_name, ordinal_position"
                cursor.execute(query)
                response = cursor.fetchall()

                # Parse response stored in dictionary
                schema = {}
                for item in response:
                    # Columns are table name, column name, data type, length
                    attrs = schema.get(item[0], [])
                    attrs.append(item[1])
                    schema[item[0]] = attrs

                # To log our database
                print("Database schema as follow: ")
                for t, table in enumerate(schema):
                    print(t + 1, table, schema.get(table))

                self.interface.setSchema(schema)

        except Exception as e:
            print(str(e))
            print("Retrieval of Schema information is unsuccessful!")