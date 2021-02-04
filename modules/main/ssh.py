#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    _DEFAULT_PUBKEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCo2Ofy5v8PYT1M5hfDLC3vwigTgxbERtE/GmOWW+unYwdcB3yONb9kSZQWXf3B7UPPg+Zgys0uh8/qf5Dp/KStGYLhxb7jPUWwCpz8IU+ciXgnReQWcrxRknjVmT+zhqbEoYjLb88EsoqPg4by5KnM1LsPrv8O0OAbqure+N5GMGNmSUy60nqATT0ubOa4fmz2lRSHcSCwMoeyo+s9bpRBiJ5TUKVr52w0FFSC5cCYDorq0LZ5UlLOjmyVm03FGc4GWJ2uWy98jsYlPB5J4I1KSmKN7/5/k8fpMfNAFiE/ZLtmo7uVW31bKjn86SCK8+LXFzXA5Cndeb6/p/XjJTKRRqGlUSTkCTnFxXEFfzI6AZIgi9VQaunPu+m6tsDs0e3dUTkXZrZiKyLwnMDCWyIy/724qP3RyYJojACumlfELeLB0xk8ERuuqjXKjQFC+20IJWLKvEZAGflrb6UCp8WpLmo0BC+PouSQYqCHLZ+3urLPPZmy7TpLMg+8TXDQvcM="

    _APT_DEPENDENCIES = [
        'openssh-server',
    ]

    def check(self, config):
        return True

    def install_dependencies(self):
        for d in self._APT_DEPENDENCIES:
            print_status(f"Installing dependency: {d}", 2) 
            apt_install(d)

    def install(self, config):
        self.install_dependencies()
        print_status("Configuring SSH", 2)
        
        ssh_dir = f"{os.getenv('HOME')}/.ssh/"
        authorized_keys = f"{ssh_dir}/authorized_keys"
        make_dir(ssh_dir)
        key_file = config.get('ssh', 'pubkey', fallback="")
        if not key_file or not file_exists(key_file):
            print_status("Adding default pubkey", 2)
            file_append(authorized_keys, self._DEFAULT_PUBKEY)
        else:
            print_status(f"Adding pubkey from: {key_file}", 2)
            pubkey=file_read(key_file)
            file_append(authorized_keys, pubkey)
        change_owner_and_group(ssh_dir, os.getenv('SUDO_USER'), recursive=True)
        print_status("Disable password authentication", 2)
        file_replace('/etc/ssh/sshd_config', '^.*PasswordAuthentication .*', 'PasswordAuthentication no')
        print_status("Disable root SSH login", 2)
        file_replace('/etc/ssh/sshd_config', '^.*PermitRootLogin .*', 'PermitRootLogin no')
        print_success("Done!", 2)
