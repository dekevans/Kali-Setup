#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        return True

    def install(self, config):
        if command_exists('tmux'):
            print_success('tmux already installed', 2)
        else:
            print_status("Installing tmux...", 2)
            apt_install('tmux')
            print_success('tmux installed', 2)

        if command_exists('xclip'):
            print_success('xclip already installed', 2)
        else:
            print_status("Installing xclip...", 2)
            apt_install('xclip')
            print_success('xclip installed', 2)

        print_status('Configuring tmux', 2)
        tmux_url = 'https://raw.githubusercontent.com/samfelt/dotfiles/master/variants/kali.tmux.conf'
        tmux_dest = get_home_folder() + '/.tmux.conf'
        file_download(tmux_url, tmux_dest)
        change_owner_and_group(tmux_dest, get_user())
        
