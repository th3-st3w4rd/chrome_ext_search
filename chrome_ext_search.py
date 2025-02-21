"""
This is a BLue Team utility used to find local Chrome extension IDs.
"""
import os, platform, json, sys
from pathlib import Path
from time import sleep
import logging
import argparse

import requests
import lxml
from bs4 import BeautifulSoup

from supported_browsers import browser_lookup

logging.basicConfig(
    filename='chrome_ext_search.log', 
    encoding='utf-8',
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filemode='w')

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

def discover_chrome_extensions(system, online_search=False):
    results = {}
    if system == "windows":
        results.update({"windows_results":{}})
        home_env = Path(os.environ["LOCALAPPDATA"])
        google_profile_locs = home_env.joinpath("Google","Chrome","User Data")
        dir_items = os.listdir(google_profile_locs)
        local_results = search_chrome_locally(google_profile_locs, dir_items)
        if online_search:
            results["windows_results"].update({"online":{}})
            for profile in local_results.keys():
                results["windows_results"]["online"].update({profile:{}})
                for ext_ids in local_results[profile].keys():
                    ext_name = search_google_web_store(extension_id=ext_ids)
                    results["windows_results"]["online"][profile].update({ext_ids:ext_name})
        else:
            results["windows_results"].update({"offline": local_results})
            
    elif system == "darwin":
        raise Exception("Extension search is not support on Apple/Mac devices.")
    
    return results

def search_edge_locally():
    pass

def search_microsoft_edge_webstore(extension_id):
    target = f"https://microsoftedge.microsoft.com/addons/detail/search/{extension_id}"

def discover_edge_extension(system, online_search=False):
    results = {}
    if system == "windows":
        results.update({"windows_results":{}})
        home_env = Path(os.environ["LOCALAPPDATA"])
        google_profile_locs = home_env.joinpath("Google","Chrome","User Data")
        dir_items = os.listdir(google_profile_locs)
        local_results = search_chrome_locally(google_profile_locs, dir_items)
        if online_search:
            results["windows_results"].update({"online":{}})
            for profile in local_results.keys():
                results["windows_results"]["online"].update({profile:{}})
                for ext_ids in local_results[profile].keys():
                    ext_name = search_microsoft_edge_webstore(extension_id=ext_ids)
                    results["windows_results"]["online"][profile].update({ext_ids:ext_name})
        else:
            results["windows_results"].update({"offline": local_results})
            
    elif system == "darwin":
        raise Exception("Extension search is not support on Apple/Mac devices.")
    
    return results



def main():
    parser= argparse.ArgumentParser()
    parser.add_argument("-o", "--online", action="store_true", help="Searches online.")
    parser.add_argument("-c", "--chrome", action="store_true", help="Searches locally for Google Chrome extensions.")
    parser.add_argument("-e", "--edge", action="store_true", help="Searches locally for Microsoft Edge extensions.")
    parser.add_argument("-f", "--fire-fox", action="store_true", help="Searches locally for Mozilla FireFox extensions.")
    parser.add_argument("-a", "--all-system-users", action="store_true", help="Searches entire system, not just current user.")
    args = parser.parse_args()
    host_os = detect_os()
    if args.chrome:
        print(json.dumps(discover_chrome_extensions(host_os, args.online), indent=4))
    if args.edge:
        print(discover_edge_extension(host_os, args.online))
    # online, browsers = set_options()
    # # print(online_search)
    # # print(browser_type)
    # final_results = extension_discovery(system=host_os, browser_types=browsers, online_search=online)
    # print(json.dumps(final_results, indent=4))

if __name__ == "__main__":
    main()