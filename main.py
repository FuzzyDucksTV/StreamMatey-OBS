"""
The `main.py` script is the entry point for the StreamMatey OBS Plugin software. It integrates all the components of the software and orchestrates their interactions to automate the process of creating video clips during a live streaming session based on chat activity and sentiment.

The script begins by setting up logging and defining several parameters for the OBS connection, the activity monitor, the sentiment analyzer, and the database.

In the `main` function, the script initializes a connection to OBS using the `obswebsocket` library. It then checks if authentication is required for the OBS WebSocket plugin and retrieves the OBS password from the environment variables.

The script also initializes the Twitch API and retrieves the user's information, including the access token, username, and channel for the Twitch chat connection.

Next, the script initializes several components of the software:

- `Database`: A SQLite database for storing and retrieving chat messages and their sentiment scores.
- `ChatConnector`: A component for connecting to the Twitch chat and retrieving messages.
- `SentimentAnalyzer`: A component for analyzing the sentiment of chat messages.
- `ActivityMonitor`: A component for monitoring chat activity.
- `ClipCreator`: A component for creating video clips in OBS.

After connecting to the Twitch chat, the script enters its main loop. In each iteration of the loop, the script retrieves a chat message, checks if its sentiment score is in the database, and if not, analyzes its sentiment and stores the score in the database. It then updates the activity monitor with the new message.

If the chat activity and sentiment score exceed their respective thresholds, the script creates a clip using the `ClipCreator` component.

The script also includes error handling to log any exceptions that occur during the loop and continue with the next iteration.

In the `__main__` section of the script, the `main` function is run using `asyncio.run`, which runs the function as an asynchronous task.

Overall, the `main.py` script serves as the central hub of the StreamMatey OBS Plugin software, coordinating the various components and managing the flow of data between them to automate the clip creation process based on chat activity and sentiment.
"""
import asyncio
import logging
import os
from obswebsocket import obsws, requests
from chat_connector import ChatConnector
from sentiment_analyzer import SentimentAnalyzer
from activity_monitor import ActivityMonitor
from clip_creator import ClipCreator
from database import Database
from twitch_api import TwitchAPI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OBS connection parameters
OBS_HOST = 'localhost'
OBS_PORT = 4444

# Activity monitor parameters
ACTIVITY_WINDOW_SIZE = 60  # seconds
ACTIVITY_THRESHOLD = 50  # messages per minute

# Sentiment analyzer parameters
SENTIMENT_THRESHOLD = 0.05  # positive sentiment score

# Database parameters
DATABASE_PATH = 'chat_messages.db'

async def main():
    # Initialize OBS WebSocket connection
    obs = obsws(OBS_HOST, OBS_PORT)
    obs.connect()

    # Get OBS WebSocket settings
    settings = obs.call(requests.GetAuthRequired())
    if not settings.isAuthRequired:
        logger.error('Please enable authentication in the OBS WebSocket plugin settings and restart the script.')
        return

    # OBS password
    OBS_PASSWORD = os.getenv('OBS_PASSWORD')

    # Initialize Twitch API
    twitch_api = TwitchAPI()  # Assuming you have a TwitchAPI class that handles Twitch API requests

    # Get Twitch user info
    twitch_user_info = twitch_api.get_user_info()  # Assuming you have a method for retrieving the user's info

    # Twitch chat connection parameters
    TWITCH_CHAT_TOKEN = twitch_user_info['access_token']
    TWITCH_CHAT_USERNAME = twitch_user_info['username']
    TWITCH_CHAT_CHANNEL = twitch_user_info['channel']

    # Initialize components
    database = Database(DATABASE_PATH)
    chat_connector = ChatConnector(TWITCH_CHAT_TOKEN, TWITCH_CHAT_USERNAME, TWITCH_CHAT_CHANNEL)
    sentiment_analyzer = SentimentAnalyzer(database)
    activity_monitor = ActivityMonitor(ACTIVITY_WINDOW_SIZE)
    clip_creator = ClipCreator(OBS_HOST, OBS_PORT, OBS_PASSWORD)

    # Connect to Twitch chat
    await chat_connector.connect()

    # Main loop
    while True:
        try:
            # Get a chat message
            message = await chat_connector.get_message()

            # Check if the message is in the database
            sentiment_score = database.get_sentiment_score(message)
            if sentiment_score is None:
                # If not, analyze the sentiment of the message
                sentiment_score = sentiment_analyzer.analyze_sentiment(message)
                # Store the sentiment score in the database
                database.store_sentiment_score(message, sentiment_score)

            # Update the activity monitor with the new message
            activity_monitor.update(message)

            # Check if the activity and sentiment thresholds are exceeded
            if activity_monitor.get_activity() > ACTIVITY_THRESHOLD and sentiment_score > SENTIMENT_THRESHOLD:
                # If so, create a clip
                clip_creator.create_clip()

            # Wait a bit before the next iteration
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            continue

if __name__ == '__main__':
    asyncio.run(main())
