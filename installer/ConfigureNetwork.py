#
#
#    Author: Ankit Jain <ankitja@vmware.com>

import os
import string
import random
import sys
import glob
import modules.commons
from jsonwrapper import JsonWrapper
from menu import Menu
from window import Window
from windowstringreader import WindowStringReader
from actionresult import ActionResult

class ConfigureNetwork(object):
    def __init__(self, install_config, maxy=0, maxx=0):
        self.install_config = install_config
        self.alpha_chars = list(range(65, 91))
        self.alpha_chars.extend(range(97, 123))
        self.hostname_accepted_chars = self.alpha_chars
        self.hostname_accepted_chars.extend(range(48, 58))
        self.ipcidr_accepted_chars = self.hostname_accepted_chars.copy()
        self.ip_accepted_chars = self.hostname_accepted_chars.copy()
        self.hostname_accepted_chars.extend([ord('.'), ord('-')])
        self.ipcidr_accepted_chars.extend([ord('.'), ord('/')])
        self.ip_accepted_chars.extend([ord('.')])
        self.random_id = '%12x' % random.randrange(16**12)
        self.random_hostname = "photon-" + self.random_id.strip()
        if 'working_directory' in self.install_config:
            self.working_directory = self.install_config['working_directory']
        else:
            self.working_directory = "/mnt/photon-root"
        self.photon_root = self.working_directory + "/photon-chroot"

        if 'ui_install' not in self.install_config:
            return

        self.maxx = maxx
        self.maxy = maxy
        self.win_width = 80
        self.win_height = 13
        self.win_starty = (self.maxy - self.win_height) // 2
        self.win_startx = (self.maxx - self.win_width) // 2
        self.menu_starty = self.win_starty + 3
        self.load_menu_list()
        self.window = Window(self.win_height, self.win_width, self.maxy, self.maxx,
                             'Configure the Network', True, action_panel=self.package_menu,
                             can_go_next=True, position=1)

    def load_menu_list(self):
        self.package_menu_items = []
        options = [
            "Retry Network autoconfiguration",
            "Retry Network autoconfiguration with a DHCP hostname",
            "Configure Network Manually", "Do not configure network manually"
        ]
        for opt in options:
            self.package_menu_items.append((opt, self.exit_function, [opt]))
        self.package_menu = Menu(self.menu_starty, self.maxx, self.package_menu_items,
                                 default_selected=0, tab_enable=False)

    @staticmethod
    def validate_hostname(hostname):
        if hostname is None or len(hostname) == 0:
            return False, "Empty hostname or domain is not allowed"

        fields = hostname.split('.')
        for field in fields:
            if not field:
                return False, "Empty hostname or domain is not allowed"
            if field[0] == '-' or field[-1] == '-':
                return False, "Hostname or domain should not start or end with '-'"

        machinename = fields[0]
        if len(machinename) > 64 or not machinename[0].isalpha():
            return False, "Hostname should start with alpha char and <= 64 chars"

        return True, None

    @staticmethod
    def validate_ipaddr(ip):
        if ip is None or len(ip) == 0:
            return False, "IP address cannot be empty"

        cidr = None
        if '/' in ip:
            ip, cidr = ip.split('/')

        octets = ip.split('.')
        if len(octets) != 4:
            return False, "Invalid IP; Must be of the form: xxx.xxx.xxx.xxx"

        for octet in octets:
            if not octet or not octet.isdigit() or ((int(octet) < 0) or (int(octet) > 255)):
                return False, "Invalid IP; Digit should be between (0 <= x <= 255)"

        if cidr is not None:
            if not cidr.isdigit() or int(cidr) >= 32 or int(cidr) <= 0:
                return False, "Invalid CIDR number!"

        return True, None

    def _execute_modules(self, phase, mod_file=None):
        """
        Execute the scripts in the modules folder
        """
        flag = False
        if mod_file is None:
            mod_file = 'm_*.py'
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "modules")))
        modules_paths = glob.glob(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')) + '/' + mod_file)
        with open('out.txt', 'a+') as f:
            print("About to call :\n",file=f)
            print(modules_paths,file=f)
        for mod_path in modules_paths:
            module = os.path.splitext(os.path.basename(mod_path))[0]
            with open('out.txt', 'a+') as f:
                print("\nNow call :\n",file=f)
                print(module,file=f)
            try:
                __import__(module)
                mod = sys.modules[module]
            except ImportError:
                modules.commons.log(modules.commons.LOG_ERROR,
                                    'Error importing module {}'.format(module))
                continue

            # the module default is disabled
            if not hasattr(mod, 'enabled') or mod.enabled is False:
                modules.commons.log(modules.commons.LOG_INFO,
                                    "module {} is not enabled".format(module))
                continue
            # check for the install phase
            if not hasattr(mod, 'install_phase'):
                modules.commons.log(modules.commons.LOG_ERROR,
                                    "Error: can not defind module {} phase".format(module))
                continue
            if mod.install_phase != phase:
                modules.commons.log(modules.commons.LOG_INFO,
                                    "Skipping module {0} for phase {1}".format(module, phase))
                continue
            if not hasattr(mod, 'execute'):
                modules.commons.log(modules.commons.LOG_ERROR,
                                    "Error: not able to execute module {}".format(module))
                continue
            result = mod.execute(self.install_config, "/")
            if result != 0:
                flag = True
        if flag == False:
            return 0
        else:
            return 1

    def exit_function(self, selected_item_params):
        items = []
        index = 0
        flag = False
        self.install_config['configu'] = selected_item_params[0]
        self.install_config.pop('vlan_id', None)
        if self.install_config['configu'] == "Retry Network autoconfiguration" or self.install_config['configu'] == "Do not configure network manually":
                result = self._execute_modules(modules.commons.PRE_INSTALL_CONFIG_AUTO, 'm_autoconfig.py')
                if result != 0:
                    return ActionResult(False, {'custom': False})

        elif self.install_config['configu'] == "Retry Network autoconfiguration with a DHCP hostname":
            dhcp_hostname_reader = WindowStringReader(
                self.maxy, self.maxx, 13, 80,
                'dhcphostname',
                None, # confirmation error msg if it's a confirmation text
                None, # echo char
                self.hostname_accepted_chars, # set of accepted chars
                ConfigureNetwork.validate_hostname, # validation function of the input
                None, # post processing of the input field
                'Choose the DHCP hostname for your system', 'DHCP Hostname:', 2, self.install_config,
                self.random_hostname,
                True)
            items.append((dhcp_hostname_reader.get_user_string, True))
            result = items[0][0](None)
            if result.success:
                pass
                #self._execute_modules(modules.commons.POST_INSTALL)
        elif self.install_config['configu'] == "Configure Network Manually":
            while True:
                ip_addr_reader = WindowStringReader(
                    self.maxy, self.maxx, 13, 80,
                    'ipaddr',
                    None, # confirmation error msg if it's a confirmation text
                    None, # echo char
                    self.ipcidr_accepted_chars, # set of accepted chars
                    ConfigureNetwork.validate_ipaddr, # validation function of the input
                    None, # post processing of the input field
                    'Choose the IP Address for your system', 'IP Address :', 2, self.install_config,
                    None,
                    True)
                items.append((ip_addr_reader.get_user_string, True))
                #with open('out.txt', 'w') as f:
                #    print(items,file=f)
                #result = items[index][0](None)
                #if result.success:
                #    #self._execute_modules(modules.commons.POST_INSTALL)
                #    pass
                #index = index + 1
                netmask_reader = WindowStringReader(
                    self.maxy, self.maxx, 13, 80,
                    'netmask',
                    None, # confirmation error msg if it's a confirmation text
                    None, # echo char 
                    self.ip_accepted_chars, # set of accepted chars
                    ConfigureNetwork.validate_ipaddr, # validation function of the input
                    None, # post processing of the input field
                    'Choose the Netmask for your system', 'Netmask :', 2, self.install_config,
                    None,
                    True)
                items.append((netmask_reader.get_user_string, True))
                #result = items[index][0](None)
                #if result.success:
                #    #self._execute_modules(modules.commons.POST_INSTALL)
                #    pass
                #else:
                #    #result = items[index-1][0](None)
                #index = index + 1
                gateway_reader = WindowStringReader(
                    self.maxy, self.maxx, 13, 80,
                    'gateway',
                    None, # confirmation error msg if it's a confirmation text
                    None, # echo char 
                    self.ip_accepted_chars, # set of accepted chars
                    ConfigureNetwork.validate_ipaddr, # validation function of the input
                    None, # post processing of the input field
                    'Choose the Gateway for your system', 'Gateway :', 2, self.install_config,
                    None,
                    True)
                items.append((gateway_reader.get_user_string, True))
                #result = items[index][0](None)
                #if result.success:
                #    #self._execute_modules(modules.commons.POST_INSTALL)
                #    pass
                #index = index + 1
                namespace_server_reader = WindowStringReader(
                    self.maxy, self.maxx, 13, 80,
                    'namespace_server',
                    None, # confirmation error msg if it's a confirmation text
                    None, # echo char 
                    self.ip_accepted_chars, # set of accepted chars
                    ConfigureNetwork.validate_ipaddr, # validation function of the input
                    None, # post processing of the input field
                    'Choose the Namespace Server for your system', 'Namespace Server :', 2, self.install_config,
                    None,
                    True)
                items.append((namespace_server_reader.get_user_string, True))
                #break
                index = 0
                while True:
                    if ((index == 1) and ('ipaddr' in self.install_config) and ('/' in str(self.install_config['ipaddr']))):
                        index += 1
                        continue
                    else:
                        result = items[index][0](None)
                    if result.success:
                        index += 1
                        if index == len(items):
                            break
                    else:
                        index -= 1
                        while index >= 0 and items[index][1] is False:
                            index -= 1
                        if index < 0:
                            flag = True
                            index = 0
                            break
                if flag == True:
                    return ActionResult(False, {'custom': False})
                    #self.load_menu_list()
                #result = items[index][0](None)
                #if result.success:
                self.install_config.pop('vlan_id', None)
                check = self._execute_modules(modules.commons.PRE_INSTALL_CONFIG)
                if check == 0:
                    break
                else:
                    return ActionResult(False, {'custom': False})
                    #continue

        return ActionResult(True, {'custom': False})

    def display(self, params):
        return self.window.do_action()
