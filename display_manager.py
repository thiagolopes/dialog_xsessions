"""
This script generate a output to execute a Desktop Environment (DE) - with Xorg and Wayland Support.

author: Thiago Lopes (TLP)
e-mail: thiagolopes at protonmail dot com

---

Copyright (C) 2023 - Thiago Lopes

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
DIALOG_CMD = "dialog"
SPC = " "
WAYLAND_SETUP = "XDG_SESSION_TYPE=wayland dbus-run-session" + SPC
XORG_SETUP = "XDG_SESSION_TYPE=x11 startx" + SPC


class DialogMenu:
    """
    A class for creating and displaying a dialog menu using the 'dialog' command-line tool.
    """
    def __init__(self, title, header, width, height, lines=0):
        self.cmd = f"{DIALOG_CMD};--title;{title};--menu;{header};{height};{width};{lines}".split(";")

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

class DesktopParser:
    cp = configparser.ConfigParser()

    def read(self, file_path):
        self.cp.read(file_path)
        humable_name = self.cp["Desktop Entry"]["Name"]
        executable = self.cp["Desktop Entry"]["Exec"]
        executable = self.get_absolute_path(executable) or executable
        return humable_name, executable

    def get_absolute_path(self, binary):
        path = shutil.which(binary)
        if not path:
            return None
        return path

if __name__ == "__main__":
    dp = DesktopParser()
    if not dp.get_absolute_path(DIALOG_CMD):
        print(f"{DIALOG_CMD=} not found", file=sys.stderr)
        sys.exit(1)

    menu = DialogMenu("Menu", "Select the desktop:", 60, 10)
    x_sessions_files = [f"{XSESSIONS_PATH}/{f}" for f in os.listdir(XSESSIONS_PATH)]
    wayland_files = [f"{WAYLAND_SESSIONS_PATH}/{f}" for f in os.listdir(WAYLAND_SESSIONS_PATH)]
    sessions_available = OrderedDict()

    for xfile in x_sessions_files:
        xhumable_name, xexecutable = dp.read(xfile)
        sessions_available[xhumable_name] = XORG_SETUP + xexecutable
    for wfile in wayland_files:
        whumable_name, wexecutable = dp.read(wfile)
        sessions_available[whumable_name] = WAYLAND_SETUP + wexecutable

    menu_result = menu.ask(list(sessions_available.keys()))
    choice = sessions_available[menu_result]
    print(choice, flush=True) # stdout
