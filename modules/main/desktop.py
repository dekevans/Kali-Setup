#!/usr/bin/env python3

from lib.automation import *
from pwd import getpwnam
import dbus


class InstallerTemplate:

    def check(self, config):
        return True

    def install(self, config):

        print_status('Copying wallpaper', 2)
        wallpaper_dir = '/usr/share/wallpapers/Custom'
        wallpaper_name = config.get('desktop', 'wallpaper', fallback = "")
        make_dir(wallpaper_dir)
        wallpaper_file = wallpaper_dir+"/"+wallpaper_name
        images_dir=os.path.dirname(os.path.realpath(__file__))+"/../../images"
        file_copy(images_dir+"/"+wallpaper_name, wallpaper_file)

        new_de = config.get('desktop', 'default desktop env', fallback="")
        if new_de != "":
            print_status(f"Installing desktop environment: {new_de}", 2)
            if new_de == "kde":
                apt_install("kali-desktop-kde")
                run_command('update-alternatives --set x-session-manager /usr/bin/startplasma-x11')
                print_status(f"Setting wallpaper", 2)
                jscript = """
                var allDesktops = desktops();
                print (allDesktops);
                for (i=0;i<allDesktops.length;i++) {
                    d = allDesktops[i];
                    d.wallpaperPlugin = "%s";
                    d.currentConfigGroup = Array("Wallpaper", "%s", "General");
                    d.writeConfig("Image", "file://%s")
                }
                """
                plugin = 'org.kde.image'
                os.seteuid(getpwnam(os.getenv('SUDO_USER')).pw_uid)
                bus = dbus.SessionBus()
                plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
                plasma.evaluateScript(jscript % (plugin, plugin, wallpaper_file))
                os.seteuid(getpwnam(os.getenv('USER')).pw_uid)
            elif new_de == "xfce":
                apt_install("kali-desktop-xfce")
                run_command('update-alternatives --set x-session-manager /usr/bin/startxfce4')
                prop="/backdrop/screen0/monitorVirtual1/workspace0/last-image"
                run_command(f"xfconf-query -c xfce4-desktop -p {prop} -s {wallpaper_file}", as_user=True)
            elif new_de == "gnome":
                apt_install("kali-desktop-gnome")
                run_command('update-alternatives --set x-session-manager /usr/bin/gnome-session')
            elif new_de == "i3":
                apt_install("kali-desktop-i3")
            elif new_de == "lxde":
                apt_install("kali-desktop-lxde")
                run_command('update-alternatives --set x-session-manager /usr/bin/startlxde')
            else:
                print_error("Unknown desktop option...",2)
            print_success("Done!", 2)

