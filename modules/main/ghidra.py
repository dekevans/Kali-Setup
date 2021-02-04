#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    _APT_DEPENDENCIES = [
        'default-jdk',
    ]

    def check(self, config):
        return True

    def install_dependencies(self):
        for d in self._APT_DEPENDENCIES:
            print_status(f"Installing dependency: {d}", 2) 
            apt_install(d)

    def install(self, config):
        print_status("Installing Ghidra", 2)
        self.install_dependencies()
        ghidra_link = run_command_with_output('curl -s "https://ghidra-sre.org/" | grep \'Download Ghidra\' | cut -d\\" -f6', safe=True).strip()
        file_download(f"https://ghidra-sre.org/{ghidra_link}", "/opt/ghidra.zip")
        run_command('cd /opt/; unzip ghidra*.zip')
        run_command('rm /opt/ghidra*.zip')
        owner = os.getenv('SUDO_USER')
        change_owner_and_group("/opt/ghidra_*_PUBLIC", owner, recursive=True)
        print_success("Done!", 2)
