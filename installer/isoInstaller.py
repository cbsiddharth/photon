#! /usr/bin/python3
#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

from argparse import ArgumentParser
import curses
from installercontainer import InstallerContainer
from iso_config import IsoConfig

class IsoInstaller(object):
    def __init__(self, stdscreen, options_file, ks_file=None):
        maxy = 0
        maxx = 0

        if stdscreen is not None:
            self.screen = stdscreen
            # Init the colors
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
            curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
            curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)

            self.screen.bkgd(' ', curses.color_pair(1))

            maxy, maxx = self.screen.getmaxyx()
            self.screen.addstr(maxy - 1, 0, '  Arrow keys make selections; <Enter> activates.')
            curses.curs_set(0)

        config = IsoConfig()
        rpm_path, install_config = config.Configure(options_file, ks_file, maxy, maxx)

        if stdscreen is not None:
            self.screen.clear()

        installer = InstallerContainer(install_config, maxy, maxx, True,
                                       rpm_path=rpm_path, log_path="/var/log")

        installer.install(None)

if __name__ == '__main__':
    usage = "Usage: %prog [options]"
    parser = ArgumentParser(usage)
    parser.add_argument("-j", "--json-file", dest="options_file", default="input.json")
    parser.add_argument('-k', "--ks-config", dest="ks_file")
    options = parser.parse_args()
    if options.ks_file:
        IsoInstaller(None, options.options_file, options.ks_file)
    else:
        curses.wrapper(IsoInstaller, options.options_file)
