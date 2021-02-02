#!/usr/bin/env python3

"""
Check if there is internet access
"""

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        #TODO: Check for ping
        return True

    def install(self, config):
        is_dry_run = config.get('general', 'dry run', fallback=False)

        print_status("Checking internet access", 2)
        ret = run_command('ping -c 1 -W 10 www.google.com', safe=True, show_error=False)
        if is_dry_run:
            ret = 0
        if ret != 0:
            print_error("No internet access! Can't continue without internet!")
            sys.exit(1)
        else:
            print_success("Looks good, internet works", 2)
