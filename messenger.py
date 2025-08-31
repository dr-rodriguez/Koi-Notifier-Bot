# Code to handle logic for communicating with Discord
# Example from https://github.com/Rapptz/discord.py/blob/master/examples/background_task.py

import os
from discord.ext import tasks

import discord
from dotenv import load_dotenv

load_dotenv()

# Get some variables
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))


class DiscordClient(discord.Client):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    # Not sure if this will work
    async def send_message(self, channel, message):
        channel = self.get_channel(channel, message)
        await channel.send(message)

    @tasks.loop(seconds=60)  # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(CHANNEL_ID)  # channel ID goes here
        
        # Tell the type checker that this is a messageable channel
        assert isinstance(channel, discord.abc.Messageable)

        self.counter += 1
        await channel.send(str(self.counter))
        # <@USER_ID>  # mention a user by their id

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in



