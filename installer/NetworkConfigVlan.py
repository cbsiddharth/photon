#    Author: Ajay Kaher <akaher@vmware.com>

import os
import sys
import subprocess
import glob
#from glob import glob
from window import Window
from textpane import TextPane
import modules.commons
from actionresult import ActionResult
from windowstringreader import WindowStringReader
from ConfigureNetwork import ConfigureNetwork

class NetworkConfigVlan(object):

    def __init__(self, install_config, maxy=0, maxx=0):
        self.install_config = install_config
        self.digit_list = list(range(48, 58))

        self.maxy = maxy
        self.maxx = maxx
        self.accepted_digit = self.digit_list
        self.default_vlanid = ""

        with open('out.txt', 'a+') as f:
            print("In the main file :\n",file=f)
        self._execute_modules(modules.commons.PRE_INSTALL_CONFIG_BACKUP, 'm_backup.py')

    @staticmethod
    def validate_vlanid(vlanid):
        if vlanid is None or not vlanid:
            return False, "Empty VLAN ID is not allowed !!"

        if ((int(vlanid) < 1) or (int(vlanid) > 4094)):
            return False, "Incorrect VLAN ID !! Digit should be between (1 <= x <= 4094)"

        return True, None

    def display_network_config_options(self):
        items = []
        self.config_network_window.hide_window()
        configure_network = ConfigureNetwork(self.install_config, self.maxy, self.maxx)
        items.append((configure_network.display, True))
        result = items[0][0](None)
        if result.success:
            return ActionResult(True, None)
        else:
            return self.display_config_network(True)

    def display_config_network(self, params):
        self.disk_buttom_items = []
        self.disk_buttom_items.append(('<Yes>', self.display_vlanid_screen, True))
        self.disk_buttom_items.append(('<No>', self.display_network_config_options, True))

        text_height = 14
        self.text_pane = TextPane((self.maxy - text_height) // 2, self.maxx, 70,
                                  "vlan.txt", text_height, self.disk_buttom_items,
                                  install_config=self.install_config)

        self.config_network_window = Window(20, 80, self.maxy, self.maxx,
                             'Configure the network via VLAN', False, action_panel=self.text_pane)
        self._execute_modules(modules.commons.PRE_INSTALL_CONFIG_VLAN, 'm_setupbeforevlan.py')
        self.install_config.pop('vlan_id', None)
        self.install_config.pop('ipaddr', None)
        self.install_config.pop('netmask', None)
        self.install_config.pop('gateway', None)
        self.install_config.pop('namespace_server', None)
        #self.config_network_window.set_action_panel(self.text_pane)
        return self.config_network_window.do_action()


    def _execute_modules(self, phase, mod_file):
        """
        Execute the scripts in the modules folder
        """
        flag = False
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
            
    def networkconfig_using_vlanid(self, result=None):
        if 'ui_install' in self.install_config:
            if (result.result != None and 'goBack' in result.result and result.result['goBack']):
                return result
            self._execute_modules(modules.commons.PRE_INSTALL_CONFIG_VLAN, 'm_setupvlan.py')

        VLAN_No = self.install_config['vlan_id']
        filename = "/etc/systemd/network/99-dhcp-en.network"
        with open(filename, "r") as f:
            buf = f.readlines()

        with open(filename, "w") as f:
            for line in buf:
                if line == "[Network]\n":
                    line = line + "VLAN=eth0." + VLAN_No + "\n"
                f.write(line)

        filename = "/etc/systemd/network/99-dhcp-en.vlan_" + VLAN_No + ".netdev"
        with open(filename, "w") as f:
            f.write("[NetDev]\n")
            f.write("Name=eth0." + VLAN_No + "\n")
            f.write("Kind=vlan\n")
            f.write("\n")
            f.write("[VLAN]\n")
            f.write("Id=" + VLAN_No + "\n")

        filename = "/etc/systemd/network/99-dhcp-en.vlan_" + VLAN_No + ".network"
        with open(filename, "w") as f:
            f.write("[Match]\n")
            f.write("Name=eth0." + VLAN_No + "\n")
            f.write("\n")
            f.write("[Network]\n")
            f.write("DHCP=yes\n")
            f.write("IPv6AcceptRA=no\n")

        cmd = "systemctl restart systemd-networkd"
        process = subprocess.Popen(cmd, shell=True)
        retval = process.wait()
        if retval != 0:
            print("Failed: systemctl restart systemd-networkd\n")

        return result

    def display_vlanid_screen(self):
        self.config_network_window.hide_window()
        vlan_id_reader = WindowStringReader(
            self.maxy, self.maxx, 15, 75,
            'vlan_id',
            None, # confirmation error msg if it's a confirmation text
            None, # echo char
            self.accepted_digit, # set of accepted chars
            NetworkConfigVlan.validate_vlanid, # validation function of the input
            None, # post processing of the input field
            '[!] Configure the network', 'If the network interface is directly connected to a VLAN trunk port,\nspecifying a VLAN ID may be necessary to get a working connection.\n\nVLAN ID (1-4094):', 
            6, 
            self.install_config,
            self.default_vlanid,
            True)
        result = self.networkconfig_using_vlanid(vlan_id_reader.get_user_string(True))
        if (result.result != None and 'goBack' in result.result and result.result['goBack']):
            return self.display_config_network(True)
        return result        
