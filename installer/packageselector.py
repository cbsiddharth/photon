#
#
#    Author: Mahmoud Bassiouny <mbassiouny@vmware.com>

import os
from jsonwrapper import JsonWrapper
from menu import Menu
from window import Window
from actionresult import ActionResult
from pprint import pprint

class PackageSelector(object):
    def __init__(self, maxy, maxx, install_config, options):
        self.install_config = install_config
        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 50
        self.win_height = 13

        self.win_starty = (self.maxy - self.win_height) // 2
        self.win_startx = (self.maxx - self.win_width) // 2

        self.menu_starty = self.win_starty + 3

        self.load_package_list(options)

    @staticmethod
    def get_packages_to_install(packagelist_file, output_data_path):
        json_wrapper_package_list = JsonWrapper(os.path.join(output_data_path, packagelist_file))
        package_list_json = json_wrapper_package_list.read()
        return package_list_json["packages"]

    @staticmethod
    def get_additional_files_to_copy_in_iso(install_option, base_path):
        additional_files = []
        if "additional-files" in install_option[1]:
            additional_files = install_option[1]["additional-files"]
        return additional_files

    def load_package_list(self, options):
        self.package_menu_items = []
        base_path = options['base_path']
        options.pop('base_path', None)
        package_list = []

        self.default_selected = 0
        visible_options_cnt = 0
        for install_option in options.items():
            if install_option[1]["visible"] == True:
                package_list = self.get_packages_to_install(install_option[1]['packagelist_file'], base_path)
                additional_files = self.get_additional_files_to_copy_in_iso(install_option, base_path)
                self.package_menu_items.append((install_option[1]["title"],
                                                self.exit_function,
                                                [install_option[0],
                                                 package_list, additional_files]))
                if install_option[0] == 'minimal':
                    self.default_selected = visible_options_cnt
                visible_options_cnt = visible_options_cnt + 1

    def exit_function(self, selected_item_params):
        self.install_config['type'] = selected_item_params[0]
        self.install_config['packages'] = selected_item_params[1]
        self.install_config['additional-files'] = selected_item_params[2]
        return ActionResult(True, {'custom': False})

    def custom_packages(self, params):
        return ActionResult(True, {'custom': True})

    def display(self, params):
        package_menu = Menu(self.menu_starty, self.maxx, self.package_menu_items,
                            default_selected=self.default_selected, tab_enable=False)
        window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                        'Select Installation', True, action_panel=package_menu,
                        can_go_next=True, position=1)
        return window.do_action()
