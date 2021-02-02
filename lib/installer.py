#!/usr/bin/env python3

from lib.printer import *
from lib.automation import *
import sys
import glob
import importlib.util


class Installer:
    def __init__(self, config):
        self._config = config
        self._all_modules  = {}
        self._pre_modules  = {}
        self._main_modules = {}
        self._post_modules = {}


    def run(self):
        print_status("Starting installer...")

        self.load_modules()
        total_module_count = (len(self._pre_modules) 
                           +  len(self._main_modules) 
                           +  len(self._post_modules))
        print_status(f"{total_module_count} Modules loaded!")
        print_status(f"{len(self._pre_modules)} Pre-Modules", 1)
        print_status(f"{len(self._main_modules)} Main Modules", 1)
        print_status(f"{len(self._post_modules)} Post-Modules", 1)

        list_of_pre_modules = [x.strip() for x in self._config.get_config()['general'].get('pre_modules').split(',')]
        list_of_main_modules = [x.strip() for x in self._config.get_config()['general'].get('main_modules').split(',')]
        list_of_post_modules = [x.strip() for x in self._config.get_config()['general'].get('post_modules').split(',')]
        main_ok_modules = []
        print_status(f"Checking {len(list_of_main_modules)} main installation modules...")

        for mod in list_of_main_modules:
            if mod not in self._main_modules:
                print_error(f"Unknown module provided: {mod}", 1)
            else:
                mod_ret = self._main_modules[mod].check(self._config.get_config())
                if mod_ret is not True:
                    print_error(f"Module {mod} error: {mod_ret}", 1)
                else:
                    main_ok_modules.append(mod)
        if len(list_of_main_modules) != len(main_ok_modules):
            print_error(f"{len(list_of_main_modules)-len(main_ok_modules)} main modules were invalid!")
            if get_input("Do you want to continue without those?", 'y', ['y','n']) != 'y':
                print_status("Exiting!")
                sys.exit(1)
            else:
                print_status("Ignoring bad modules, continuing!")
        else:
            print_success("Modules are good to go!")
        print_status("Executing Pre-Modules...")
        print_status(f"Running {len(self._pre_modules)} Pre-Modules!", 1)       
        #TODO: Need to sort modules to a proper order
        self.run_modules(list_of_pre_modules, self._pre_modules)
        print_success("Done with Pre-Modules")
        print_status("Executing Main Modules...")
        print_status(f"Running {len(main_ok_modules)} main installation modules!", 1)       
        self.run_modules(main_ok_modules, self._main_modules)
        print_status("Done with Main Modules")
        quit()


        print_status("Executing post-module scripts...")
        self.after_modules()
        print_success("Done with post-module scripts")
        print_success("Done installing!")


    def load_modules(self):
        for fileloc in glob.glob('modules/pre/*.py'):
            if '__init__' not in fileloc:
                module_name = fileloc.replace('/', '.')[:-3]
                type_name = module_name.split('.')[-1]
                spec = importlib.util.spec_from_file_location(module_name, fileloc)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self._pre_modules[type_name] = mod.InstallerTemplate()

        for fileloc in glob.glob('modules/main/*.py'):
            if '__init__' not in fileloc:
                module_name = fileloc.replace('/', '.')[:-3]
                type_name = module_name.split('.')[-1]
                spec = importlib.util.spec_from_file_location(module_name, fileloc)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self._main_modules[type_name] = mod.InstallerTemplate()

        for fileloc in glob.glob('modules/post/*.py'):
            if '__init__' not in fileloc:
                module_name = fileloc.replace('/', '.')[:-3]
                type_name = module_name.split('.')[-1]
                spec = importlib.util.spec_from_file_location(module_name, fileloc)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self._post_modules[type_name] = mod.InstallerTemplate()

        self._all_modules['pre']  = self._pre_modules
        self._all_modules['main'] = self._main_modules
        self._all_modules['post'] = self._post_modules

    def run_modules(self, list_of_modules, module_installers):
        is_dry_run = self._config.get_config().get('general', 'dry run', fallback=False)
        if list_of_modules[0] == 'all':
            list_of_modules = module_installers.keys()        

        counter = 1
        for mod in list_of_modules:
            print_status(f"[{counter}/{len(list_of_modules)}] Running module: {mod}...", 1)
            try:
                module_installers[mod].install(self._config.get_config())
            except Exception as e:
                print_error(f"Module '{mod}' had runtime error: {e}", 1)
            print_success(f"Done with {mod}!", 1)
            counter += 1

    def after_modules(self):
        default_shell = self._config.get_config().get('general', 'default shell', fallback="")
        if default_shell != "":
            print_status("Setting default shell to {0}...".format(default_shell), 1)
            path = run_command_with_output('which {0}'.format(default_shell)).strip()
            if path == "":
                print_error("Invalid shell: '{0}'".format(default_shell), 1)
            else:
                run_command('chsh -s "{0}" "{1}"'.format(path, get_user()))
                run_command('chsh -s "{0}" root'.format(path))
                print_success("Done!", 1)
    
