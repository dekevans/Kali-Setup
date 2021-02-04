#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    _REPOS_TO_ADD = {
    }

    _PACKAGES = {
        "APT HTTPS": ["apt-transport-https"],
        "gnupg": ['gnupg'],
        "bash completion": ['bash-completion'],
        "tmux": ["tmux"],
        "Compressors and decompressors": ["unzip", "zip", "p7zip-full"],
        "nmap": ["nmap"],
        "gdp-peda": ["gdb-peda"],
        "SSH Server": ["openssh-server"],
        "SecLists": ['seclists'],
    }

    _COMMANDS_BEFORE = {
    }

    _COMMANDS_AFTER = {
    }

    def check(self, config):
        return True

    def install(self, config):
        print_status("Executing pre-install commands...", 2)
        for title,cmds in self._COMMANDS_BEFORE.items():
            print_status(f"{title}...", 2)
            for cmd in cmds:
                run_command(cmd)
            print_success("Done!",2)
        print_success("Done executing pre-install commands", 2)

        print_status("Adding new repositories", 2)
        for name,repo in self._REPOS_TO_ADD.items():
            file_write(f"/etc/apt/sources.list.d/{name}.list", repo)

        print_status("Updating repos before starting installs", 2)
        run_command("apt update")

        print_status("Installing packages!", 2)
        for title,pkgs in self._PACKAGES.items():
            print_status(f"Installing {title}...", 2)
            apt_install(pkgs)
            print_success("Done!",2)
        print_success("Done installing packages!", 2)

        print_status("Executing post-install commands...", 2)
        for title, cmds in self._COMMANDS_AFTER.items():
            print_status(f"{title}...", 2)
            for cmd in cmds:
                run_command(cmd)
            print_success("Done!", 2)
        print_success("Done executing post-install commands", 2)



