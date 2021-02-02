#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        return True

    def install(self, config):
        is_dry_run = config.getboolean('general', 'dry run', fallback=False)
        latest_kernel = config.getboolean('general', 'latest kernel', fallback=True)

        print_status("Checking if we are running as the latest kernel", 2)
        if latest_kernel and not is_dry_run:
            val = run_command_with_output('dpkg -l | grep linux-image- | grep -vc meta')
            if int(val) > 1:
                print_status("Detected {0} kernels".format(val.strip()), 2)
                val = run_command("dpkg -l | grep linux-image | grep -v meta | sort -t '.' -k 2 -g | tail -n 1 | grep \"$(uname -r)\"", show_error=False)
                if val == 0:
                    print_success("You are running the latest kernel!  All good", 2)
                    print_status("Installing the latest kernel headers", 2)
                    run_command('apt -y -qq install make gcc "linux-headers-$(uname -r)"')
                    print_success("Done", 2)
                else:
                    print_error("You are not running the latest kernel but its installed already!", 2)
                    print_error("Reboot and then re-run this script!")
                    sys.exit(1)
        else:
            print_success("Skipping!", 2)

