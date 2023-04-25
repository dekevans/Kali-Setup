# Kali Setup Script

This has been forked from [samfelt](https://github.com/samfelt/Kali-Setup), who forked from [Raikia](github.com/raikia/Kali-Setup), who credits
[g0tmi1k](https://github.com/g0tmi1k/os-scripts) with the original script.
Basically there's a long line of smart people's work that this has been built
on top of. I'm doing what I can to make this as usable and functional as
possible but the meat of how these modules work is not my own creation.

## Basic Usage

```
python3 kali-setup.py
```

To know more about the available arguments use `--help`

```
usage: kali_setup.py [-h] [--list-modules] [-g] [-c config_file] [--run-module module] [-v] [--dry-run] [--no-pre] [--no-post]

optional arguments:
  -h, --help            show this help message and exit
  --list-modules        List availbe modules
  -g, --generate        Generate config file
  -c config_file, --config config_file
                        Configuration file to use
  --run-module module   Run individual module
  -v, --verbose         Be mor verbose with output
  --dry-run             Don't actually download anything
  --no-pre              Don't run any Pre-Modules
  --no-post             Don't run any Post-Modules
```

## Configuration

The default configuration file is `setup_config.ini`, this will be used if no
other is specified. Use this file to configure exactly what modules you want to
run and any more specific options those modules might have. To have every
module in a specific category run, you can put `all` in the configuration file.

The `--verbose` or `--dry-run` arguments will override what has been set in the
configuration file.

## Running an individual module

To run just one module, use the `--run-module` argument. This will jump
straight to installing that module, skipping all the checks and every other
module. The module you want to run has to be supplied in the
`<category>.<module>` format. For example, if you wanted to only install
`ghidra` from the main set of modules you would run:

```
python3 kali-setup.py --run-module main.ghidra
```

And if for some reason you just wanted to check internet access you could run:

```
python3 kali-setup.py --run-module pre.internet
```
