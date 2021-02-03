#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        return True

    def install(self, config):
        new_de = config.get('general', 'default desktop env', fallback="")
        if new_de != "":
            print_status(f"Installing desktop environment: {new_de}", 2)
            if new_de == "kde":
                apt_install("kali-desktop-kde")
                run_command('update-alternatives --set x-session-manager /usr/bin/startplasma-x11')
            elif new_de == "xfce":
                apt_install("kali-desktop-xfce")
                run_command('update-alternatives --set x-session-manager /usr/bin/startxfce4')
            elif new_de == "gnome":
                apt_install("kali-desktop-gnome")
                run_command('update-alternatives --set x-session-manager /usr/bin/gnome-session')
            elif new_de == "i3":
                apt_install("kali-desktop-i3")
            elif new_de == "lxde":
                apt_install("kali-desktop-lxde")
                run_command('update-alternatives --set x-session-manager /usr/bin/startlxde')
            else:
                print_error("Unknown desktop option...",2)
            print_success("Done!", 2)

