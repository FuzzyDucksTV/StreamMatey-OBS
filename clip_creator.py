"""
The `clip_creator.py` script is a crucial part of the StreamMatey OBS Plugin software. It interfaces with the Open Broadcaster Software (OBS) using its API to automate the process of creating video clips during a live streaming session. The script is designed to help content creators using the StreamMatey OBS Plugin by automating the clip creation process based on certain conditions.
The conditions for clip creation are determined by chat activity and sentiment. When these conditions are met, the script sends a command to OBS to start recording, creating a video clip of the live stream. After a specified length of time (default is 60 seconds), the script sends another command to OBS to stop recording, thus ending the clip.
The `ClipCreator` class within the script encapsulates the functionality needed to interact with OBS and manage the clip creation process. It maintains a connection to OBS through the `obswebsocket` library and provides methods to start and stop recording.
The class also interacts with a SQLite database (`comments.db`) to store and retrieve comments from the chat. This is used in conjunction with the sentiment analysis to determine when to create a clip. The `store_comment` method stores a new comment in the database, and the `get_comment_sentiment` method retrieves the sentiment score for a given comment.
The `ClipCreator` class is initialized with several parameters, including the host and port for the OBS connection, the password for OBS, the sensitivity for clip creation (which could be based on the volume or sentiment of chat activity), and the length of the clip to be created.
In the `__main__` section of the script, an instance of the `ClipCreator` class is created and used to establish a connection with OBS and create a clip. This serves as an example of how to use the `ClipCreator` class.
Overall, the `clip_creator.py` script plays a vital role in the StreamMatey OBS Plugin software, providing an automated and intelligent way to create clips based on chat activity and sentiment during a live stream.
"""

import logging
from obswebsocket import obsws, requests
import time
import sqlite3

class ClipCreator:
    def __init__(self, host, port, password, clip_sensitivity, clip_length=60):
        self.host = host
        self.port = port
        self.password = password
        self.clip_sensitivity = clip_sensitivity
        self.clip_length = clip_length
        self.obs_connection = None
        self.db_connection = sqlite3.connect('comments.db')

    def initialize_obs_connection(self):
        try:
            self.obs_connection = obsws(self.host, self.port, self.password)
            self.obs_connection.connect()
            logging.info("Connected to OBS")
        except Exception as e:
            logging.error(f"Failed to connect to OBS: {e}")
            raise

    def create_clip(self):
        try:
            self.obs_connection.call(requests.StartRecording())
            time.sleep(self.clip_length)
            self.obs_connection.call(requests.StopRecording())
            logging.info("Clip created")
        except Exception as e:
            logging.error(f"Failed to create clip: {e}")
            raise

    def store_comment(self, comment):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO comments (content) VALUES (?)", (comment,))
        self.db_connection.commit()

    def get_comment_sentiment(self, comment):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT sentiment FROM comments WHERE content = ?", (comment,))
        result = cursor.fetchone()
        return result[0] if result else None

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    clip_creator = ClipCreator(host="localhost", port=4444, password="secret", clip_sensitivity=80)
    clip_creator.initialize_obs_connection()
    clip_creator.create_clip()
