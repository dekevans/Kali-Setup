#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        return True

    def install(self, config):
        metapackage = config.get('general', 'metapackage', fallback="")
        if metapackage != "":
            print_status(f"Installing metapackage: {metapackage}", 2)
            if metapackage == "default":
                apt_install("kali-linux-default")
            elif metapackage == "large":
                apt_install("kali-linux-large")
            elif metapackage == "everything":
                apt_install("kali-linux-everything")
            else:
                print_error("Unknown metapackage...", 2)
            print_success("Done!", 2)

