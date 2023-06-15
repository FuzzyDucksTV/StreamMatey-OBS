"""
The `activity_monitor.py` script is part of the StreamMatey OBS Plugin software. It provides an `ActivityMonitor` class for tracking chat activity and a `Bot` class for interacting with Twitch chat.

The `ActivityMonitor` class is responsible for monitoring the rate of chat messages. It uses a deque to store the timestamps of the most recent messages within a specified window size.

The `ActivityMonitor` class has two methods:

- `add_message(message)`: Adds the timestamp of a new message to the deque.
- `get_activity_level()`: Calculates and returns the current activity level, defined as the number of messages per second.

The `Bot` class is a subclass of `commands.Bot` from the `twitchio.ext` module. It extends the base class with an `activity_monitor` attribute and overrides the `event_message` method to add each incoming message to the activity monitor.

The `Bot` class also includes a command for checking the current activity level. The `activity_command` method responds to the "!activity" command by printing the current activity level.

In the main part of the script, an `ActivityMonitor` instance and a `Bot` instance are created. The `ActivityMonitor` instance is set to monitor a 1-minute window of activity. The `Bot` instance is initialized with the necessary Twitch credentials and the `ActivityMonitor` instance, and is set to join two channels.

Finally, the bot is run with the `run` method. This starts the bot and begins monitoring chat activity.
"""

import asyncio
import collections
import time
from twitchio.ext import commands

class ActivityMonitor:
    def __init__(self, window_size):
        self.window_size = window_size
        self.timestamps = collections.deque(maxlen=window_size)

    def add_message(self, message):
        self.timestamps.append(time.time())

    def get_activity_level(self):
        if len(self.timestamps) < 2:
            return 0
        time_diff = self.timestamps[-1] - self.timestamps[0]
        return len(self.timestamps) / time_diff if time_diff else 0

class Bot(commands.Bot):
    def __init__(self, irc_token, client_id, nick, prefix, initial_channels, activity_monitor):
        super().__init__(irc_token=irc_token, client_id=client_id, nick=nick, prefix=prefix, initial_channels=initial_channels)
        self.activity_monitor = activity_monitor

    async def event_message(self, message):
        print(message.content)
        self.activity_monitor.add_message(message)

    @commands.command(name='activity')
    async def activity_command(self, ctx):
        activity_level = self.activity_monitor.get_activity_level()
        print(f'Activity level: {activity_level} messages per second')

if __name__ == "__main__":
    window_size = 60  # 1 minute window
    activity_monitor = ActivityMonitor(window_size)

    bot = Bot(
        irc_token='oauth:YOUR_IRC_TOKEN',
        client_id='YOUR_CLIENT_ID',
        nick='YOUR_NICK',
        prefix='!',
        initial_channels=['channel1', 'channel2'],
        activity_monitor=activity_monitor
    )
    bot.run()
