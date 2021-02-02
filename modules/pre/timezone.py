#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        return True

    def install(self, config):
        print_status("Setting timezone", 2)
        timezone =config.get('general', 'timezone', fallback="")
        if timezone == '' or not file_exists(f"/usr/share/zoneinfo/{timezone}"):
            print_error(f"'{timezone}'' is not a valid timezone!", 2)
            if get_input('Do you want to still continue?', 'y', ['y','n']).lower() == 'n':
                print_success("Exiting!")
                sys.exit(1)
            print_success("Skipping!", 2)
        else:
            file_write('/etc/timezone', timezone)
            run_command(f'ln -sf "/usr/share/zoneinfo/{timezone}" /etc/localtime')
            run_command('dpkg-reconfigure -f noninteractive tzdata')
            print_success("Done!", 2)

