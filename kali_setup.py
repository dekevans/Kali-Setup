#!/usr/bin/env python3

import sys
import os
import subprocess
import argparse
import glob
from lib.printer import print_success,print_error
from lib import config
from lib import installer

def compile_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--list-modules", action="store_true",
                        help="List availbe modules")
    parser.add_argument("-g", "--generate", action="store_true",
                        help="Generate config file")
    parser.add_argument("-c", "--config", metavar="config_file",
                       default="setup_config.ini",
                       help="Configuration file to use")
    parser.add_argument("--run-module", metavar="module",
                        help="Run individual module")
    parser.add_argument("-v", "--verbose", action = "store_true",
                        help="Be mor verbose with output")
    parser.add_argument("--dry-run", action="store_true",
                        help="Don't actually download anything")
    parser.add_argument("--no-pre", action="store_true",
                        help="Don't run any Pre-Modules")
    parser.add_argument("--no-post", action="store_true",
                        help="Don't run any Post-Modules")
    return parser.parse_args()

def list_modules():
    pre_modules_dir = 'modules/pre'
    main_modules_dir = 'modules/main'
    post_modules_dir = 'modules/post'
    print("Pre Modules:")
    print("------------------")
    for fileloc in glob.glob(f"{pre_modules_dir}/*.py"):
        if '__init__' not in fileloc:
            module_name = fileloc.split('/')[-1][:-3]
            print(f"  {module_name}")
    print("")
    print("Main Modules:")
    print("------------------")
    for fileloc in glob.glob(f"{main_modules_dir}/*.py"):
        if '__init__' not in fileloc:
            module_name = fileloc.split('/')[-1][:-3]
            print(f"  {module_name}")
    print("")
    print("Post Modules:")
    print("------------------")
    for fileloc in glob.glob(f"{post_modules_dir}/*.py"):
        if '__init__' not in fileloc:
            module_name = fileloc.split('/')[-1][:-3]
            print(f"  {module_name}")
    print("")

def main():
    arguments = compile_arguments()
    if arguments.list_modules:
        list_modules()
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
    conf.argument_overwrite(arguments)
    install = installer.Installer(conf)
    install.run()

if __name__ == '__main__':
    main()
