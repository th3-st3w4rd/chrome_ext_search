"""
This is a BLue Team utility used to find local Chrome extension IDs.
"""
import logging
import argparse

from supported_browsers import Chrome, Edge

logging.basicConfig(
    filename='chrome_ext_search.log', 
    encoding='utf-8',
    level=logging.INFO,
    format="%(levelname)s - %(asctime)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    filemode='w')

# def detect_os():
#     os_type = platform.system().lower()
#     return os_type

def main():
    parser= argparse.ArgumentParser()
    parser.add_argument("-o", "--online", action="store_true", help="Searches online.")
    parser.add_argument("-c", "--chrome", action="store_true", help="Searches locally for Google Chrome extensions.")
    parser.add_argument("-e", "--edge", action="store_true", help="Searches locally for Microsoft Edge extensions.")
    parser.add_argument("-f", "--fire-fox", action="store_true", help="Searches locally for Mozilla FireFox extensions.")
    parser.add_argument("-a", "--all-system-users", action="store_true", help="Searches entire system, not just current user.")
    args = parser.parse_args()
    if args.chrome:
        search = Chrome(args.online)
        print(search.discover_chrome_extensions())
    if args.edge:
        search = Edge(args.online)
        print(search.discover_edge_extension())
    # online, browsers = set_options()
    # # print(online_search)
    # # print(browser_type)
    # final_results = extension_discovery(system=host_os, browser_types=browsers, online_search=online)
    # print(json.dumps(final_results, indent=4))

if __name__ == "__main__":
    main()