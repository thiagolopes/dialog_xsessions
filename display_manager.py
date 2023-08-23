"""
This script show a menu with xsessions available
"""
import configparser
import os
import shutil
import subprocess
import sys
import tempfile
from collections import OrderedDict

XSESSIONS_PATH = "/usr/share/xsessions"
WAYLAND_SESSIONS_PATH = "/usr/share/wayland-sessions"

def sanitaze_relative_path(path):
    absolute_path = shutil.which(path)
    if not absolute_path:
        return path
    return absolute_path

class DialogMenu:
    """
    A class for creating and displaying a dialog menu using the 'dialog' command-line tool.
    """
    def __init__(self, title, header, width, height, lines=0):
        self.cmd = f"dialog;--title;{title};--menu;{header};{height};{width};{lines}".split(";")

    def enumarate_options(self, options):
        return [str(item) for sublist in enumerate(options) for item in sublist]

    def ask(self, options):
        temp_output = tempfile.TemporaryFile()
        enumarated_options = self.enumarate_options(options)

        subprocess.run(
            self.cmd + enumarated_options,
            stderr=temp_output, stdout=sys.stderr, check=True,
        )

        temp_output.seek(0)
        resp = int(temp_output.read())
        temp_output.close()
        return options[resp]


if __name__ == "__main__":
    menu = DialogMenu("Menu", "Select the desktop:", 60, 10)
    cp = configparser.ConfigParser()

    x_sessions_files = [f"{XSESSIONS_PATH}/{f}" for f in os.listdir(XSESSIONS_PATH)]
    # wayland_files = [f"{WAYLAND_SESSIONS_PATH}/{f}" for f in os.listdir(WAYLAND_SESSIONS_PATH)]

    sessions_available = OrderedDict()
    for session in x_sessions_files:
        cp.read(session)
        sessions_available[cp["Desktop Entry"]["Name"]] = cp["Desktop Entry"]["Exec"]

    menu_result = menu.ask(list(sessions_available.keys()))
    executable = sessions_available[menu_result]

    print("startx " + sanitaze_relative_path(executable), flush=True) # stdout
