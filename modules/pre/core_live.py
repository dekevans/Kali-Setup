#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        return True

    def install(self, config):
        print_status("Ensuring core and live are installed...", 2)
        apt_install(["kali-linux-core", "kali-desktop-live"])
        print_success("Done!", 2)
 
