# Code to handle logic for communicating with Discord
# Example from https://github.com/Rapptz/discord.py/blob/master/examples/background_task.py

import os

import discord
from discord import File


class DiscordClient(discord.Client):
    """
    A class to handle the core logic of sending a message to a Discord channel.
    This class is designed to be imported and used by other scripts.
    """

    def __init__(self, token, channel_id):
        self.token = token
        self.channel_id = channel_id
        self.client = discord.Client(intents=discord.Intents.default())
        self._message_to_send = None
        self._image_to_send = None

        # We need to set up the on_ready event handler as a coroutine within the class instance.
        # This is a common pattern for running a one-off task with discord.py.
        self.client.event(self.on_ready)

    async def on_ready(self):
        """
        The coroutine that runs when the client is successfully connected.
        It sends the message and then closes the connection.
        """
        print(f"{self.client.user} has successfully connected to Discord!")

        channel = self.client.get_channel(self.channel_id)
        if channel:
            try:
                # The message content is passed to the send method, not the class constructor.
                # This allows for a new message to be generated for each call.
                if self._image_to_send is not None:
                    await channel.send(self._message_to_send, file=self._image_to_send)
                else:
                    await channel.send(self._message_to_send)

                print(f"Message sent to channel {channel.name}!")
                print(f"Message content: {self._message_to_send}")
            except Exception as e:
                print(f"Failed to send message: {e}")
        else:
            print(f"Error: Could not find a channel with the ID `{self.channel_id}`.")

        await self.client.close()

    def send_message(self, message_content: str):
        """
        Public method to start the message sending process.
        It stores the message content and runs the client.
        """
        self._message_to_send = message_content
        self._image_to_send = None
        self.client.run(self.token)

    def send_message_with_image(self, message_content: str, image_path: str):
        """
        Public method to send an image to a Discord channel.
        """
        fp = open(image_path, "rb")
        self._image_to_send = File(fp, filename=os.path.basename(image_path))
        self._message_to_send = message_content
        self.client.run(self.token)
        fp.close()
