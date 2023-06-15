"""
The `chat_connector.py` script is part of the StreamMatey OBS Plugin software. It provides a `ChatConnector` class for connecting to and interacting with Twitch chat.

The `ChatConnector` class is a subclass of `commands.Bot` from the `twitchio.ext` module. It extends the base class with additional methods for handling chat events and managing the chat connection.

The `ChatConnector` class has the following methods:

- `__init__(irc_token, client_id, nick, prefix, initial_channels)`: Initializes a new instance of the `ChatConnector` class. The parameters are used to authenticate with Twitch and configure the bot.

- `event_ready()`: An event handler that is called when the bot is ready. It prints a message indicating that the bot has successfully connected to chat.

- `event_message(message)`: An event handler that is called when a new chat message is received. It prints the content of the message and then handles any commands in the message.

- `connect_to_chat()`: A method that starts the bot and manages the chat connection. If an error occurs while starting the bot, the method waits for 5 seconds and then tries to connect again.

In the main part of the script, a `ChatConnector` instance is created with the necessary Twitch credentials and a list of channels to join. The bot is then run with the `run` method. This starts the bot and begins receiving and handling chat messages.
"""
import asyncio
from twitchio.ext import commands

class ChatConnector(commands.Bot):

    def __init__(self, irc_token, client_id, nick, prefix, initial_channels):
        super().__init__(
            irc_token=irc_token,
            client_id=client_id,
            nick=nick,
            prefix=prefix,
            initial_channels=initial_channels,
        )

    async def event_ready(self):
        print(f"Successfully connected to chat as {self.nick}")

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    async def connect_to_chat(self):
        try:
            await super().start()
        except Exception as e:
            print(f"Error occurred: {e}")
            await asyncio.sleep(5)
            await self.connect_to_chat()

if __name__ == "__main__":
    irc_token = "oauth:your_oauth_token"
    client_id = "your_client_id"
    nick = "your_bot_name"
    prefix = "!"
    initial_channels = ["channel1", "channel2"]

    bot = ChatConnector(irc_token, client_id, nick, prefix, initial_channels)
    bot.run()