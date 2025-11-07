# The main application code

import argparse
import datetime
import os
import random

from bs4 import BeautifulSoup
from dotenv import load_dotenv

from fetch_lodestone import fetch_lodestone, get_black_mage_level
from messenger import DiscordClient


def ffxiv_notification():
    """Main function to set up the correct message for FFXIV"""

    # Grab the lodestone page and parse it
    html_doc = fetch_lodestone(LODESTONE_URL)
    soup = BeautifulSoup(html_doc, "html.parser")
    level = get_black_mage_level(soup)
    print("Black Mage Level:", level)

    # Number of days until patch 7.4 (December 16, 2025)
    days_until_patch = (datetime.datetime(2025, 12, 16) - datetime.datetime.now()).days

    # List of messages to choose from
    message_list = [
        # f"Hey, <@{USER_ID}>. Remember to level black mage! Current level: {level}",
        # f"Black mage is at level {level}. Keep going, <@{USER_ID}>!",
        f"Don't forget to level black mage, <@{USER_ID}>! It's currently level {level}.",
        f"You didn't forget to level black mage, did you, <@{USER_ID}>? It's at level {level} now.",
        f"Don't let us down, <@{USER_ID}>! Black mage is only level {level}. You only have {days_until_patch} days until patch 7.4!",
        f"Patch 7.4 will be here sooner than you think (just {days_until_patch} days!). Keep leveling black mage, <@{USER_ID}>! It's at level {level}.",
        f"Yoshi P will be disappointed if you don't level black mage, <@{USER_ID}>! It's currently level {level}.",
        f"Sigh... your black mage is still only level {level}, <@{USER_ID}>. You can do better. Only {days_until_patch} days until patch 7.4!",
        f"This is your weekly reminder to level black mage, <@{USER_ID}>! It's currently level {level}.",
        f"Y'shtola looks at you with disappointment, <@{USER_ID}>. Your black mage is only level {level}.",
        f"Haurchefant died so you could level black mage, <@{USER_ID}>. It's only level {level}.",
        f"Are you even trying, <@{USER_ID}>? Black mage is still level {level}. Only {days_until_patch} days until patch 7.4!",
        f"The best class in the game is black mage. Level it up, <@{USER_ID}>! It's currently level {level}. Only {days_until_patch} days until patch 7.4!",
        # f"Don't make me come over there, <@{USER_ID}>. Level your black mage! It's at level {level}.",
    ]
    # Special messages for certain levels
    if level == 0:
        message_list.extend(
            [
                f"Hey, <@{USER_ID}>, why haven't you started leveling black mage yet? It's still level 0! You only have {days_until_patch} days until patch 7.4!",
                f"Black mage is still level 0, <@{USER_ID}>. You should probably start leveling it- you only have {days_until_patch} days until patch 7.4!",
                f"Don't you want to play black mage, <@{USER_ID}>? It's still level 0! Patch 7.4 is only {days_until_patch} days away!",
                f"The clock is ticking, <@{USER_ID}>! You only have {days_until_patch} days to level black mage until patch 7.4!",
            ]
        )
    elif level > 0:
        message_list.extend(
            [
                f"Wow, <@{USER_ID}>, you actually started leveling black mage! It's level {level} now!",
                f"It's a miracle, <@{USER_ID}>! You started leveling black mage! You're at level {level}.",
            ]
        )
    elif level >= 90:
        message_list.append(
            f"Wow, <@{USER_ID}>, black mage is already level {level}! You're doing great!"
        )
    # Overwrite to a single message at level 100
    elif level == 100:
        message_list = [
            f"Congratulations, <@{USER_ID}>! You leveled black mage to 100. Now you can start playing the game!",
        ]

    # Pick random message
    message = random.choice(message_list)

    return message


def dnd_notification():
    """Main function to set up the correct message for DND"""

    # List of messages to choose from
    message_list = [
        f"Hey, <@{USER_ID}>. Time for some DnD!",
        f"It's Thursday night, <@{USER_ID}>. You know what that means! DnD time!",
        f"Don't forget, <@{USER_ID}>, it's DnD night!",
        f"Roll for initiative, <@{USER_ID}>! It's DnD time!",
        f"<@{USER_ID}>, your DnD party awaits!",
        f"Grab your dice, <@{USER_ID}>! It's time for DnD!",
        f"Prepare for adventure, <@{USER_ID}>! DnD night is here!",
        f"Your DnD friends are counting on you, <@{USER_ID}>!",
        f"Don't let your DnD party down, <@{USER_ID}>!",
        f"Get ready for some epic quests, <@{USER_ID}>! It's DnD night!",
    ]

    # Pick random message
    message = random.choice(message_list)

    return message


if __name__ == "__main__":
    # Use argparse to handle command line arguments
    parser = argparse.ArgumentParser(
        description="A bot to notify a user on a Discord channel."
    )
    parser.add_argument("--ffxiv", action="store_true", help="Send FFXIV Black Mage level notification")
    parser.add_argument("--dnd", action="store_true", help="Send DnD night notification")
    args = parser.parse_args()


    # Fetch environment variables
    load_dotenv()
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    LODESTONE_URL = os.getenv("LODESTONE_URL")
    USER_ID = int(os.getenv("USER_ID"))

    if args.ffxiv:
        # Send FFXIV notification
        message = ffxiv_notification()
        channel_id = int(os.getenv("FFXIV_CHANNEL_ID"))
    elif args.dnd:
        # Send DnD notification
        message = dnd_notification()
        channel_id = int(os.getenv("DND_CHANNEL_ID"))

    # Start the Discord client and send the message
    if message is not None and channel_id is not None:
        client = DiscordClient(token=DISCORD_TOKEN, channel_id=channel_id)
        client.send_message(message_content=message)
    else:
        print(f"Error preparing message or getting channel_id: {message}, {channel_id}")
