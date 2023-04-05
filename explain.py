from project import DatabaseCursor
import time
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

        # # On CLicked Methods for Submit Buttons
        # self.onClickedOldQueryButton()
        # self.onClickedNewQueryButton()
        #
        # # Reset Button
        # self.onClickedResetButton()

        # # Text-to-speech capabilities
        # self.player = QMediaPlayer()
        #
        # self.onClickedOldPlayButton()
        # self.onClickedOldStopButton()
        #
        # self.onClickedNewPlayButton()
        # self.onClickedNewStopButton()


    def onDatabaseChanged(self):
        self.updateSchema()

    def checkConfigFileExists(self):
        if not hasattr(self, "config") or self.config == None:
            return False

        return True

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

    # #----------------------------------- Text-to-Speech -----------------------------------------------------
    # def onClickedOldPlayButton(self):
    #     self.interface.playOldButton.clicked.connect(lambda: self.playAudioFile("oldQuery"))
    #
    # def onClickedOldStopButton(self):
    #     self.interface.stopOldButton.clicked.connect(self.stopAudioFile)
    #
    # def onClickedNewPlayButton(self):
    #     self.interface.playNewButton.clicked.connect(lambda: self.playAudioFile("newQuery"))
    #
    # def onClickedNewStopButton(self):
    #     self.interface.stopNewButton.clicked.connect(self.stopAudioFile)
    # def textToSpeech(self,text, typeOfQuery):
    #
    #     speaker = gTTS(text=text, lang="en", slow=False)
    #
    #     file_path = os.path.join(os.getcwd(), typeOfQuery + str(".mp3"))
    #     if os.path.exists(file_path):
    #         os.remove(file_path)
    #
    #     # saves the text speech as an MP3
    #     speaker.save(typeOfQuery + str(".mp3"))
    #
    #     # returns stat_result object
    #     statbuf = os.stat(typeOfQuery + str(".mp3"))
    #
    #     # statbuf.st_size -> represents the size of the file in kbytes -> convert to MBytes
    #     mbytes = statbuf.st_size / 1024
    #
    #     # MB / 200 MBPS -> to get the duration of the mp3 in seconds
    #     duration = mbytes / 200
    #
    # def stopAudioFile(self):
    #     self.player.pause()
    # def playAudioFile(self,typeOfQuery):
    #     mp3_name = typeOfQuery + str(".mp3")
    #     file_path = os.path.join(os.getcwd(), mp3_name)
    #     url = QUrl.fromLocalFile(file_path)
    #
    #     content = QMediaContent(url)
    #     self.player.setMedia(QMediaContent())  # reset the media player
    #     self.player.setMedia(content)
    #     self.player.play()
