#!/usr/bin/env python3

import sys
import os
import subprocess
import argparse
import glob
from modules.common.printer import print_success,print_error
from modules.common import config
from modules.common import installer

def compile_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-modules", action="store_true",
                        help="List availbe modules")
    parser.add_argument("-g", "--generate", action="store_true",
                        help="Generate config file")
    parser.add_argument("-c", "--config", metavar="config_file",
                       default="setup_config.ini",
                       help="Configuration file to use")
    return parser.parse_args()

def main():

    arguments = compile_arguments()
    if arguments.list_modules:
        print("Available Modules:")
        print("------------------")
        for fileloc in glob.glob('modules/templates/*.py'):
            if '__init__' not in fileloc:
                module_name = fileloc.split('/')[-1][:-3]
                print(f"  {module_name}")
        sys.exit(0)

    if os.geteuid() != 0:
        print_error("You must run this script as root!")
        print_error("Run:  sudo -E {0}".format(os.path.basename(__file__)))
        sys.exit(1)
    if os.getenv('PWD') is None:
        print_error("You have to run this script with 'sudo -E'. You are probably missing the -E parameter.")
        sys.exit(1)

    config_file = arguments.config
    if arguments.generate:
        conf = config.Config(None)
        conf.generate_config(config_file)
        print_success(f"Configuration file generated: ./{config_file}")
        sys.exit(0)

    conf = config.Config(config_file)
    conf.load_config()
    install = installer.Installer(conf)
    install.run()

if __name__ == '__main__':
    main()
