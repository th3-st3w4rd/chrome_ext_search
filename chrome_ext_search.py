"""
This is a BLue Team utility used to find local Chrome extension IDs.
"""
import os, platform, json
from pathlib import Path

def local_chrome_ext_check(system):
    if system == "windows":
        home_env = Path(os.environ["LOCALAPPDATA"])
        profile_locs = home_env.joinpath("Google","Chrome","User Data")
        dir_items = os.listdir(profile_locs)
        findings = {"results":{}}
        for item in dir_items:
            if item.startswith("Profile"):
                ext_loc = profile_locs.joinpath(item,"Extensions")
                exts = os.listdir(ext_loc)
                findings["results"].setdefault(item,exts)
        results = json.dumps(findings, indent=4)
        return results

def detect_os():
    os_type = platform.system().lower()
    return os_type

def main():
    host_os = detect_os()
    print(local_chrome_ext_check(system=host_os))

if __name__ == "__main__":
    main()