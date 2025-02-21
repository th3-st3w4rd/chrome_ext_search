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

def set_options():
    online_input = input("Would you like to search online? (y/n)").lower()
    online_search = False
    if online_input == "y":
        online_search = True
    
    if "y" not in online_input and "n" not in online_input:
        logging.error(f"Please supply a valid input.")
        logging.error(f"Epected 'y' or 'n' but got '{online_input}' instead.")

    browser_types = input("Which browsers would you like to search?\nChrome(c), Firefox(f), Safari(s), or Edge(e)? eg. 'cfse'\n").lower()
    local_browser_ext_type = {
        "chrome": False,
        "fire_fox": False,
        "safari": False,
        "edge": False,
    }

    if "c" not in browser_types and "f" not in browser_types and "s" not in browser_types and "e" not in browser_types:
        logging.error("Please supply a valid input.")
        logging.error(f"Expected 'c', 'f', 's', or 'e' but got '{browser_types}' instead.")

    for option in browser_types:
        if option == "c":
            local_browser_ext_type["chrome"] = True
        if option == "f":
            local_browser_ext_type["fire_fox"] = True
        if option == "s":
            local_browser_ext_type["safari"] = True
        if option == "e":
            local_browser_ext_type["edge"] = True

    return online_search, local_browser_ext_type

def detect_os():
    os_type = platform.system().lower()
    return os_type

def search_chrome_locally(google_profile_locs, dir_items):
    findings = {}
    for profiles in dir_items:
        if profiles.startswith("Profile"):
            findings.update({profiles:{}})
            ext_locs = [google_profile_locs.joinpath(profiles,"Extensions")]
            for loc in ext_locs:
                for exts in os.listdir(loc):
                    findings[profiles].update({exts:"n/a"})
                    logging.info(f"Found Profile: '{profiles}' Extension ID:'{exts}'")
    return findings

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

def extension_discovery(system, browser_types, online_search):
    results = {}
    if system == "windows":
        results.update({"windows_results":{}})
        home_env = Path(os.environ["LOCALAPPDATA"])
        if browser_types["chrome"]:
            google_profile_locs = home_env.joinpath("Google","Chrome","User Data")
            dir_items = os.listdir(google_profile_locs)
            local_results = search_chrome_locally(google_profile_locs, dir_items)
            if online_search:
                results["windows_results"].update({"online":{}})
                for profile in local_results.keys():
                    results["windows_results"]["online"].update({profile:{}})
                    for ext_ids in local_results[profile].keys():
                        print(ext_ids)
                        ext_name = online_results = search_google_web_store(extension_id=ext_ids)
                        results["windows_results"]["online"][profile].update({ext_ids:ext_name})
            else:
                results["windows_results"].update({"offline": local_results})
            
        if browser_types["fire_fox"]:
            pass
        if browser_types["safari"]:
            pass
        if browser_types["edge"]:
            pass

    elif system == "darwin":
        home_env = ""
        profile_locs = ""
        dir_items = ""
    
    return results




def main():
    online, browsers = set_options()
    # print(online_search)
    # print(browser_type)
    host_os = detect_os()
    final_results = extension_discovery(system=host_os, browser_types=browsers, online_search=online)
    print(json.dumps(final_results, indent=4))

if __name__ == "__main__":
    main()