"""
The `sentiment_analyzer.py` script is part of the StreamMatey OBS Plugin software. It provides functions for analyzing the sentiment of chat messages using the VADER Sentiment Analysis tool.

The script begins by importing the necessary libraries and initializing the SentimentIntensityAnalyzer from the `vaderSentiment` module. It also connects to an SQLite database where comments and their sentiment scores are stored.

The script provides the following functions:

- `analyze_sentiment(chat_message)`: This function takes a chat message as input and returns its sentiment score. It first checks if the comment exists in the database. If it does, it retrieves the sentiment score from the database. If it doesn't, it calculates the sentiment score using the SentimentIntensityAnalyzer, stores the comment and its score in the database, and then returns the score.

- `handle_api_error(e)`: This function handles any API errors that occur during sentiment analysis. It logs the error message for debugging purposes.

- `bypass_repetitive_comments(chat_messages)`: This function takes a list of chat messages and returns a list of unique messages and messages that appear more than 3 times. This is used to filter out repetitive comments and focus on the unique and frequently occurring comments for sentiment analysis.

In the main part of the script, the `nltk` library's `vader_lexicon` is downloaded for use by the SentimentIntensityAnalyzer. A table for storing comments and their sentiment scores is also created in the SQLite database if it doesn't already exist.
"""

# Libraries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import sqlite3
from collections import Counter

# Download the vader_lexicon
nltk.download('vader_lexicon')

# Initialize the SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()

# Connect to SQLite database
conn = sqlite3.connect('comments.db')
c = conn.cursor()

# Create table for storing comments
c.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        comment TEXT,
        sentiment REAL
    )
''')

def analyze_sentiment(chat_message):
    """
    This function takes in a chat message as input and returns the sentiment score.
    It first checks if the comment exists in the database. If it does, it retrieves the sentiment score from the database.
    If it doesn't, it calculates the sentiment score and stores the comment and its score in the database.
    """
    c.execute('SELECT sentiment FROM comments WHERE comment = ?', (chat_message,))
    result = c.fetchone()
    if result is not None:
        return result[0]
    else:
        sentiment_score = sid.polarity_scores(chat_message)['compound']
        c.execute('INSERT INTO comments VALUES (?, ?)', (chat_message, sentiment_score))
        conn.commit()
        return sentiment_score

def handle_api_error(e):
    """
    This function handles any API errors that occur during sentiment analysis.
    It logs the error message for debugging purposes.
    """
    print(f"API Error: {e}")

def bypass_repetitive_comments(chat_messages):
    """
    This function takes in a list of chat messages and returns a list of unique messages and messages that appear more than 3 times.
    """
    counter = Counter(chat_messages)
    return [message for message, count in counter.items() if count <= 3]
