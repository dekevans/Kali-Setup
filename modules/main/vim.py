#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        return True

    def install(self, config):
        if command_exists('vim'):
            print_success('vim already installed', 2)
        else:
            print_status("Installing vim...", 2)
            apt_install('vim')
            print_success('vim installed', 2)

        print_status('Configuring vim', 2)
        vimrc_url = 'https://raw.githubusercontent.com/samfelt/dotfiles/master/variants/kali.vimrc'
        vimrc_dest = get_home_folder() + '/.vimrc'
        file_download(vimrc_url, vimrc_dest)
        change_owner_and_group(vimrc_dest, get_user())
        
