#!/usr/bin/env python3

"""
Run updates
"""

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        #TODO: Check for apt
        return True

    def install(self, config):
        is_dry_run = config.getboolean('general', 'dry run', fallback=False)
        run_update = config.getboolean('general', 'update first', fallback=True)

        print_status("Running system updates before starting. This may take a while...", 2)
        if run_update and not is_dry_run:
            run_command("apt -y -qq clean") 
            run_command("apt -y -qq autoremove") 
            run_command("apt -y -qq update") 
            run_command('export DEBIAN_FRONTEND=noninteractive; APT_LISTCHANGES_FRONTEND=none apt -o Dpkg::Options::="--force-confnew" -y dist-upgrade --fix-missing')
            run_command("apt -y -qq clean")
            run_command("apt -y -qq autoremove")
            print_success("Done!", 2)
        else:
            print_success("Skipping!", 2)
