#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    _APT_DEPENDENCIES = [
        'git',
        'python3-pip',
    ]

    _REPOS = [
        'slimm609/checksec.sh',
        'Hackplayers/evil-winrm',
        'SecureAuthCorp/impacket',
        'ticarpi/jwt_tool',
        'Ganapati/RsaCtfTool',
        'carlospolop/privilege-escalation-awesome-scripts-suite/',
        'rebootuser/LinEnum',
    ]

    _ADDITIONAL_INSTRUCTIONS = {
        'Hackplayers/evil-winrm': ['gem install winrm winrm-fs stringio'],
        'ticarpi/jwt_tool': ['pip3 install termcolor cprint pycryptodomex requests'],
    }

    def check(self, config):
        return True if command_exists("git") else "'git' package not installed"

    def install_dependencies(self):
        for d in self._APT_DEPENDENCIES:
            print_status(f"Installing dependency: {d}", 2)
            apt_install(d)

    def install(self, config):
        self.install_dependencies()
        print_status("Installing various github tools into /opt", 2)
        user = os.getenv('SUDO_USER')
        for proj in self._REPOS:
            print_status(f"Cloning {proj}...", 2)
            folder_name = f"/opt/{proj.split('/')[1]}"
            github_clone(proj, folder_name)
            run_command("cd {0}; git pull -q".format(folder_name))
            if proj in self._ADDITIONAL_INSTRUCTIONS:
                for instr in self._ADDITIONAL_INSTRUCTIONS[proj]:
                    run_command("cd {0}; {1}".format(folder_name, instr))
            change_owner_and_group(folder_name, user, recursive=True)
            print_success("Done!", 2)
        print_success("Done installing github tools!", 2)
        
        print_status("Writing GitHub update script", 2)
        update_file_contents = """#!/bin/bash
for d in /opt/* ; do
    echo "Starting $d"
    pushd $d &> /dev/null
    git fetch
    git pull origin master
    popd &> /dev/null
done
for d in /opt/cs_scripts/* ; do
    echo "Starting $d"
    pushd $d &> /dev/null
    git fetch
    git pull origin master
    popd &> /dev/null
done"""
        file_write('/opt/UpdateAll.sh', update_file_contents)
        run_command('chmod +x /opt/UpdateAll.sh')
        change_owner_and_group('/opt/UpdateAll.sh', user)
        print_success('Done', 2)
