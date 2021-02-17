#!/usr/bin/env python3

from lib.automation import *

"""
https://github.com/Tib3rius/AutoRecon
"""

"""
Manual Install Instructions:

sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
python3 -m pip install --user pipx
python3 -m pipx ensurepath

/home/kali/.local/bin/pipx install git+https://github.com/Tib3rius/AutoRecon.git

create symlink 
ln -s /home/kali/.local/pipx/venvs/autorecon/bin/autorecon /usr/local/bin/autorecon

"""

class InstallerTemplate:

    _APT_DEPENDENCIES = [
        'python3',
        'python3-pip',
        'python3-venv',
        'seclists',
        'curl',
        'enum4linux',
        'gobuster',
        'nbtscan',
        'nikto',
        'nmap',
        'onesixtyone',
        'oscanner',
        'smbclient',
        'smbmap',
        'smtp-user-enum',
        'snmp',
        'sslscan',
        'sipvicious',
        'tnscmd10g',
        'whatweb',
        'wkhtmltopdf',
    ]

    def check(self, config):
        return True

    def install_dependencies(self):
        for d in self._APT_DEPENDENCIES:
            print_status(f"Installing dependency: {d}", 2) 
            apt_install(d)

        user = os.getenv("SUDO_USER")
        print_status(f"Checking if pipx is installed for user: {user}", 2)
        if not file_exists(f"/home/{user}/.local/bin/pipx"):
            #os.seteuid(getpwnam(os.getenv('SUDO_USER')).pw_uid)
            run_command("python3 -m pip install --user pipx", as_user=True)
            run_command("python3 -m pipx ensurepath", as_user=True)
            #os.seteuid(getpwnam(os.getenv('USER')).pw_uid)

        print_success(f"pipx is installed form: {user}", 2)

    def install(self, config):
        """
        print_status("Installing Ghidra", 2)
        self.install_dependencies()
        ghidra_link = run_command_with_output('curl -s "https://ghidra-sre.org/" | grep \'Download Ghidra\' | cut -d\\" -f6', safe=True).strip()
        file_download(f"https://ghidra-sre.org/{ghidra_link}", "/opt/ghidra.zip")
        run_command('cd /opt/; unzip ghidra*.zip')
        run_command('rm /opt/ghidra*.zip')
        owner = os.getenv('SUDO_USER')
        change_owner_and_group("/opt/ghidra_*_PUBLIC", owner, recursive=True)
        """
        print_success("Done!", 2)
