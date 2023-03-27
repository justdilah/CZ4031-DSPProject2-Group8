from project import DatabaseCursor
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys
import json

FILE_CONFIG = "config.json"
def run(self):
    self.window.show()
    list_db = list(self.config.keys())
    # print(f"List of database configs from json file: {list_db}")
    self.window.setListDatabase(list_db)
    sys.exit(self.app.exec_())

def onDatabaseChanged(UI):
    # cur_db = self.window.list_database.currentText()
    # print(f"Current selected database is {dbname}")
    # db_config = config['dbname']

    updateSchema(UI)

def updateSchema(UI):
    # if not self.hasDbConfig():
    #     self.window.setSchema(None)
    #     self.window.showError("Database configuration is not found")
    #     return
    # try:
    with open(FILE_CONFIG, "r") as file:
        config = json.load(file)
        print(config)
        db_config = config["TPC-H"]
    with DatabaseCursor(db_config) as cursor:

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

        UI.setSchema(schema)

    # except Exception as e:
    #     print(str(e))
        # self.window.showError("Unable to retrieve schema information!", e)