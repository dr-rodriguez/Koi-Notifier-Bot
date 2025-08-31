# Script to fetch data from the Lodestone webpage and parse it

import os
import urllib.request

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

# Get some variables
LODESTONE_URL = os.getenv("LODESTONE_URL")


def fetch_lodestone(url):
    # Fetch the HTML content from the Lodestone URL
    f = urllib.request.urlopen(url)
    html_doc = f.read()

    # Output to file for testing
    # with open("lodestone_koi.html", "wb") as file:
    #     file.write(html_doc)

    return html_doc


def get_job_level(soup, job_name):
    # Find the div with class 'character__job__name' and text from job_name
    job_name_div = soup.find("div", class_="character__job__name", string=job_name)

    # Get the parent <li> element
    parent_li = job_name_div.find_parent("li")

    # Find the level div within the same <li>
    level_div = parent_li.find("div", class_="character__job__level")

    if level_div.text == "-" or level_div.text == "":
        level = "0"
    else:
        level = level_div.text.strip()

    return level

def get_black_mage_level(soup):
    job = "Black Mage"

    try:
        job_level = get_job_level(soup, job)
    except AttributeError:
        job = "Thaumaturge"
        job_level = get_job_level(soup, job)

    return int(job_level)


if __name__ == "__main__":
    # Alternatively, read from a local file for testing
    with open("lodestone_koi.html", "r", encoding="utf-8") as file:
        html_doc = file.read()

    soup = BeautifulSoup(html_doc, "html.parser")
    level = get_black_mage_level(soup)
    print("Black Mage Level:", level)
