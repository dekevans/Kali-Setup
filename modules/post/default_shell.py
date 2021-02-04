#!/usr/bin/env python3

from lib.automation import *

class InstallerTemplate:

    def check(self, config):
        return True

    def install(self, config):
        default_shell = config.get('general', 'default shell', fallback="")
        if default_shell != "":
            print_status(f"Setting default shell to {default_shell}...", 2)
            path = run_command_with_output(f"which {default_shell}").rstrip()
            if path == "":
                print_error(f"Invalid shell: '{default_shell}'", 2)
            else:
                run_command(f"chsh -s '{path}' '{get_user()}'")
                run_command(f"chsh -s '{path}' root")
                print_success("Done!", 2)

