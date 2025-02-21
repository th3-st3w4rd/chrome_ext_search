"""
This is a BLue Team utility used to find local Chrome extension IDs.
"""
import os, platform, json
from pathlib import Path
from time import sleep
import logging

import requests
import lxml
from bs4 import BeautifulSoup

logging.basicConfig(
    filename='chrome_ext_search.log', 
    encoding='utf-8',
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filemode='w')

def local_chrome_ext_check(system):
    if system == "windows":
        home_env = Path(os.environ["LOCALAPPDATA"])
        profile_locs = home_env.joinpath("Google","Chrome","User Data")
        dir_items = os.listdir(profile_locs)
        findings = {}
        for profiles in dir_items:
            if profiles.startswith("Profile"):
                findings.update({profiles:{}})
                ext_locs = [profile_locs.joinpath(profiles,"Extensions")]
                for loc in ext_locs:
                    for exts in os.listdir(loc):
                        print(f"Looking at Profile: '{profiles}' Extension ID:'{exts}'")
                        name = search_google_web_store(extension_id=exts)
                        findings[profiles].update({exts:name})
        return findings

def detect_os():
    os_type = platform.system().lower()
    return os_type

def search_google_web_store(extension_id):
    try:
        logging.info(f"Searching '{extension_id}' on Google Web Store.")
        target = f"https://chromewebstore.google.com/detail/application-launcher-for/{extension_id}"
        response = requests.get(url=target).content
        soup = BeautifulSoup(response, "lxml")
        results = soup.h1.text
        ext_name = results
        logging.info(f"Extension ID: '{extension_id}' is Extension Name: '{ext_name}'")
    except Exception as e:
        logging.debug(e)
        logging.error("Could not access this item")
        ext_name = "unknown_extension"
    finally:
        sleep_time = 1
        logging.info(f"Sleeping for '{sleep_time}' seconds before sending another request.")
        sleep(sleep_time)
    return ext_name


def main():
    host_os = detect_os()
    final_results = local_chrome_ext_check(system=host_os)
    print(json.dumps(final_results, indent=4))

if __name__ == "__main__":
    main()