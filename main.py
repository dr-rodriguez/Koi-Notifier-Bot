# The main application code

import os
import random

import discord
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from fetch_lodestone import fetch_lodestone, get_black_mage_level
from messenger import DiscordClient

if __name__ == "__main__":
    # Fetch environment variables
    load_dotenv()
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    LODESTONE_URL = os.getenv("LODESTONE_URL")
    USER_ID = int(os.getenv("USER_ID"))
    CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

    # Grab the lodestone page and parse it
    html_doc = fetch_lodestone(LODESTONE_URL)
    soup = BeautifulSoup(html_doc, "html.parser")
    level = get_black_mage_level(soup)
    print("Black Mage Level:", level)

    # List of messages to choose from
    message_list = [
        f"Hey, <@{USER_ID}>. Remember to level black mage! Current level: {level}",
        f"Black mage is at level {level}. Keep going, <@{USER_ID}>!",
        f"Don't forget to level black mage, <@{USER_ID}>! It's currently level {level}.",
        f"You didn't forget to level black mage, did you, <@{USER_ID}>? It's at level {level} now.",
        f"Don't let us down, <@{USER_ID}>! Black mage is only level {level}.",
        f"Patch 7.4 will be here sooner than you think. Keep leveling black mage, <@{USER_ID}>! It's at level {level}.",
    ]
    if level == 0:
        message_list.append(f"Come on, <@{USER_ID}>, you haven't even started leveling black mage yet! It's time to get going!")
    if level >= 90:
        message_list.append(f"Wow, <@{USER_ID}>, black mage is already level {level}! You're doing great!")

    # Overwrite to a single message at level 100
    if level == 100:
        message_list = [
            f"Congratulations, <@{USER_ID}>! You leveled black mage to 100! Not you can start playing the game!",
        ]


    # Start the Discord client and send the message
    client = DiscordClient(intents=discord.Intents.default())
    client.run(CLIENT_SECRET)

    # Pick random message
    message = random.choice(message_list)

    # Send the message
    client.send_message(message)
