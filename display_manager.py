"""
This script show a menu with xsessions available
"""
import configparser
import os
import subprocess
import sys
import tempfile
from collections import OrderedDict

XSESSIONS_PATH = "/usr/share/xsessions"
# default_options will not be overwrite by XSESSIONS_PATH
DEFAULT_OPTIONS = OrderedDict({
        "X (~/.xinit)": "startx",
        "GNOME": "XDG_SESSION_TYPE=wayland dbus-run-session gnome-session", # check if dbus-launch --exit-with-session works
        "Plasma (Wayland)": "XDG_SESSION_TYPE=wayland dbus-run-session startplasma-wayland",  # experimental
})


class DialogMenu:
    """
    A class for creating and displaying a dialog menu using the 'dialog' command-line tool.
    """
    def __init__(self, title, header, width, height, lines=0):
        self.cmd = f"dialog;--title;{title};--menu;{header};{height};{width};{lines}".split(";")

    def enumarate_options(self, options):
        options = list(options)
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

    xsessions_files = [f"{XSESSIONS_PATH}/{f}" for f in os.listdir(XSESSIONS_PATH)]
    assert xsessions_files  # security check

    xsessions_available = OrderedDict(DEFAULT_OPTIONS)
    for xsession in xsessions_files:
        cp.read(xsession)
        xsessions_available.setdefault(cp["Desktop Entry"]["Name"], cp["Desktop Entry"]["Exec"])

    result = menu.ask(list(xsessions_available.keys()))
    print(xsessions_available[result], flush=True) # stdout
