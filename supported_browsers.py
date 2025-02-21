import os
from pathlib import Path
from time import sleep
import logging
import platform

import requests
from bs4 import BeautifulSoup

class Browser():
    def __init__(self, online):
        self.host_os = platform.system().lower()
        self.online = online
        self.results = {}

        if self.host_os == "windows":
            self.home_env = Path(os.environ["LOCALAPPDATA"])
        else:
            raise Exception(f"'{self.host_os}' is not supported.")
    #def create_result_structure()
    
class Chrome(Browser):
    def __init__(self, online):
        super().__init__(online)

    def discover_chrome_extensions(self):
        self.results.update({"windows_results":{}})
        google_profile_locs = self.home_env.joinpath("Google","Chrome","User Data")
        dir_items = os.listdir(google_profile_locs)
        local_results = self.search_chrome_locally(google_profile_locs, dir_items)
        if self.online:
            # use recursion to go down the tree?
            self.results["windows_results"].update({"online":{}})
            for profile in local_results.keys():
                self.results["windows_results"]["online"].update({profile:{}})
                for ext_ids in local_results[profile].keys():
                    ext_name = self.search_google_web_store(extension_id=ext_ids)
                    self.results["windows_results"]["online"][profile].update({ext_ids:ext_name})
        else:
            self.results["windows_results"].update({"offline": local_results})

        return self.results
    
    def search_chrome_locally(self, google_profile_locs, dir_items):
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

    def search_google_web_store(self,extension_id):
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
    
class Edge(Browser):
    def __init__(self, online):
        super().__init__(online)

    def search_edge_locally(self):
        #maybe this should be like a formatting.
        pass

    def search_microsoft_edge_webstore(self, extension_id):
        target = f"https://microsoftedge.microsoft.com/addons/detail/search/{extension_id}"

    def discover_edge_extension(self, online_search=False):
        # results = {}
        # if system == "windows":
        self.results.update({"windows_results":{}})
        home_env = Path(os.environ["LOCALAPPDATA"])
        edge_profile_locs = home_env.joinpath("Microsoft","Edge","User Data","Default","Extensions")
        dir_items = os.listdir(edge_profile_locs)
        print(dir_items)
        # local_results = self.search_edge_locally(edge_profile_locs, dir_items)
        # if online_search:
        #     results["windows_results"].update({"online":{}})
        #     for profile in local_results.keys():
        #         results["windows_results"]["online"].update({profile:{}})
        #         for ext_ids in local_results[profile].keys():
        #             ext_name = self.search_microsoft_edge_webstore(extension_id=ext_ids)
        #             results["windows_results"]["online"][profile].update({ext_ids:ext_name})
        # else:
        #     results["windows_results"].update({"offline": local_results})
        
        # return results
