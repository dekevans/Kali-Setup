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


    def run_one(self, module_string):
        s = module_string.split('.')
        category = s[0]
        mod = s[1]
        if category not in ['pre', 'main', 'post']:
            print_error(f"{category} is not a valid category")
            sys.exit(1)
        self.load_modules()
        module_set = f"{category}_modules"
        list_of_modules = [x.strip() for x in self._config.get_config()['general'].get(module_set).split(',')]
        if list_of_modules[0] == 'all':
            list_of_modules = list(self._all_modules[category].keys())
        if mod not in list_of_modules:
            print_error(f"{category} is not a module in in the '{mod}' category")
            sys.exit(1)

        print_status(f"Running module: {mod}...", 1)
        try:
            self._all_modules[category][mod].install(self._config.get_config())
        except Exception as e:
            print_error(f"Module '{mod}' had runtime error: {e}", 1)
        print_success(f"Done with {mod}!", 1)

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

        list_of_modules = {}
        list_of_modules['pre']  = [x.strip() for x in self._config.get_config()['general'].get('pre_modules').split(',')]
        if list_of_modules['pre'][0] == 'all':
            list_of_modules['pre'] = list(self._pre_modules.keys())
        priority = open('modules/pre/priority.txt').read().splitlines()
        list_of_modules['pre'] = self.sort_lists(list_of_modules['pre'], priority)

        list_of_modules['main'] = [x.strip() for x in self._config.get_config()['general'].get('main_modules').split(',')]
        if list_of_modules['main'][0] == 'all':
            list_of_modules['main'] = list(self._main_modules.keys())
        priority = open('modules/main/priority.txt').read().splitlines()
        list_of_modules['main'] = self.sort_lists(list_of_modules['main'], priority)

        list_of_modules['post'] = [x.strip() for x in self._config.get_config()['general'].get('post_modules').split(',')]
        if list_of_modules['post'][0] == 'all':
            list_of_modules['post'] = list(self._post_modules.keys())
        priority = open('modules/post/priority.txt').read().splitlines()
        list_of_modules['post'] = self.sort_lists(list_of_modules['post'], priority)

        main_ok_modules = []

        for time,modules in list_of_modules.items():
            if modules == ['']:
                list_of_modules[time] = []

        print_status(f"Checking {len(list_of_modules['main'])} main installation modules...")

        for mod in list_of_modules['main']:
            if mod not in self._main_modules:
                print_error(f"Unknown module provided: {mod}", 1)
            else:
                mod_ret = self._main_modules[mod].check(self._config.get_config())
                if mod_ret is not True:
                    print_error(f"Module {mod} error: {mod_ret}", 1)
                else:
                    main_ok_modules.append(mod)
        if len(list_of_modules['main']) != len(main_ok_modules):
            print_error(f"{len(list_of_modules[main])-len(main_ok_modules)} main modules were invalid!")
            if get_input("Do you want to continue without those?", 'y', ['y','n']) != 'y':
                print_status("Exiting!")
                sys.exit(1)
            else:
                print_status("Ignoring bad modules, continuing!")
        else:
            print_success("Modules are good to go!")

        if len(list_of_modules['pre']) != 0:
            print_status("Executing Pre-Modules...")
            print_status(f"Running {len(list_of_modules['pre'])} Pre-Modules!", 1)       
            #TODO: Need to sort modules to a proper order
            self.run_modules(list_of_modules['pre'], self._pre_modules)
            print_success("Done with Pre-Modules")
        else:
            print_success("No Pre-Modules to run")

        print_status("Executing Main Modules...")
        print_status(f"Running {len(main_ok_modules)} main installation modules!", 1)       
        self.run_modules(main_ok_modules, self._main_modules)
        print_status("Done with Main Modules")

        if len(list_of_modules['post']) != 0:
            print_status("Executing Post-Modules...")
            print_status(f"Running {len(list_of_modules['post'])} Post-Modules!", 1)       
            #TODO: Need to sort modules to a proper order
            self.run_modules(list_of_modules['post'], self._post_modules)
            print_success("Done with Post-Modules")
        else:
            print_success("No Post-Modules to run")


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
        if len(list_of_modules) == 0:
            #print_status("No modules to run")
            return
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

    def sort_lists(self, unsorted_list, priority):
        run_first = [x for x in unsorted_list if x in priority]
        run_second= [x for x in unsorted_list if x not in priority]
        run_first.sort(key = lambda x: priority.index(x))
        return run_first + run_second


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
    
