import os
import subprocess
import shlex
import re
import json
import time
import crypt
import string
from urllib.request import urlopen
import random
import requests
import cracklib
import modules.commons
from partitionISO import PartitionISO
from packageselector import PackageSelector
from windowstringreader import WindowStringReader
from jsonwrapper import JsonWrapper
from selectdisk import SelectDisk
from license import License
from linuxselector import LinuxSelector
from ostreeserverselector import OSTreeServerSelector
from ostreewindowstringreader import OSTreeWindowStringReader
from NSXAplianceConfig import NSXAplianceConfig
from NetworkConfigVlan import NetworkConfigVlan
from ConfigureNetwork import ConfigureNetwork

class IsoConfig(object):
    g_ostree_repo_url = None
    """This class handles iso installer configuration."""
    def __init__(self):
        self.cd_mount_path = None
        self.alpha_chars = list(range(65, 91))
        self.alpha_chars.extend(range(97, 123))
        self.hostname_accepted_chars = self.alpha_chars
        # Adding the numeric chars
        self.hostname_accepted_chars.extend(range(48, 58))
        # Adding the . and -
        self.hostname_accepted_chars.extend([ord('.'), ord('-')])
        self.random_id = '%12x' % random.randrange(16**12)
        self.random_hostname = "photon-" + self.random_id.strip()
        self.install_config = {}

    def Configure(self, options_file, ks_file, maxy, maxx):
        ks_path = ks_file
        rpm_path = None
        ks_config = None
        cd_search = None

        with open('/proc/cmdline', 'r') as f:
            kernel_params = shlex.split(f.read().replace('\n', ''))

        for arg in kernel_params:
            if arg.startswith("ks=") and ks_path is None:
                ks_path = arg[len("ks="):]
            elif arg.startswith("repo="):
                rpm_path = arg[len("repo="):]
            elif arg.startswith("photon.media="):
                cd_search = arg[len("photon.media="):]

        if cd_search is not None:
            self.mount_cd(cd_search)

        if ks_path is not None:
            ks_config = self.get_config(ks_path)

        if rpm_path is None:
            # the rpms should be in the cd
            if self.cd_mount_path is None:
                raise Exception("Please specify RPM repo location, as no cdrom is specified. (PXE?)")
            rpm_path = os.path.join(self.cd_mount_path, "RPMS")

        self.install_config['iso_system'] = False # not creating iso system
        self.install_config['iso_config'] = self.parse_config_file('iso.cfg')
        if ks_config:
            self.ks_config(options_file, ks_config)
        else:
            self.install_config['ui_install'] = True
            self.ui_config(options_file, maxy, maxx)

        return rpm_path, self.install_config

    @staticmethod
    def is_vmware_virtualization():
        """Detect vmware vm"""
        process = subprocess.Popen(['systemd-detect-virt'], stdout=subprocess.PIPE)
        out, err = process.communicate()
        if err is not None and err != 0:
            return False
        return out.decode() == 'vmware\n'

    def get_config(self, path):
        """kick start configuration"""
        if path.startswith("http://"):
            # Do 5 trials to get the kick start
            # TODO: make sure the installer run after network is up
            ks_file_error = "Failed to get the kickstart file at {0}".format(path)
            wait = 1
            for _ in range(0, 5):
                err_msg = ""
                try:
                    response = requests.get(path, timeout=3)
                    if response.ok:
                        return json.loads(response.text)
                    err_msg = response.text
                except Exception as e:
                    err_msg = e

                modules.commons.log(modules.commons.LOG_ERROR,
                                    ks_file_error)
                modules.commons.log(modules.commons.LOG_ERROR,
                                    "error msg: {0}".format(err_msg))
                print(ks_file_error)
                print("retry in a second")
                time.sleep(wait)
                wait = wait * 2

            # Something went wrong
            print(ks_file_error)
            print("exiting the installer, check the logs for more details")
            raise Exception(err_msg)
        else:
            if path.startswith("cdrom:/"):
                if self.cd_mount_path is None:
                    raise Exception("cannot read ks config from cdrom, no cdrom specified")
                path = os.path.join(self.cd_mount_path, path.replace("cdrom:/", "", 1))
            return (JsonWrapper(path)).read()

    def mount_cd(self, cd_search):
        """Mount the cd with RPMS"""
        # check if the cd is already mounted
        if self.cd_mount_path:
            return
        mount_path = "/mnt/cdrom"

        cmdline = ["umount", "/mnt/cdrom"]
        process = subprocess.Popen(cmdline)
        retval = process.wait()

        # Mount the cd to get the RPMS
        os.makedirs(mount_path, exist_ok=True)

        # Construct mount cmdline
        cmdline = ['mount']
        if cd_search.startswith("UUID="):
            cmdline.extend(['-U', cd_search[len("UUID="):] ]);
        elif cd_search.startswith("LABEL="):
            cmdline.extend(['-L', cd_search[len("LABEL="):] ]);
        elif cd_search == "cdrom":
            cmdline.append('/dev/cdrom')
        else:
            print("Unsupported installer media, check photon.media in kernel cmdline")
            raise Exception("Can not mount the cd")

        cmdline.extend(['-o', 'ro', mount_path])

        # Retry mount the CD
        for _ in range(0, 3):
            process = subprocess.Popen(cmdline)
            retval = process.wait()
            if retval == 0:
                self.cd_mount_path = mount_path
                return
            print("Failed to mount the cd, retry in a second")
            time.sleep(1)
        print("Failed to mount the cd, exiting the installer")
        print("check the logs for more details")
        raise Exception("Can not mount the cd")

    def ks_config(self, options_file, ks_config):
        """Load configuration from file"""
        del options_file

        # Merge contents of ks_config into install_config
        for k, v in ks_config.items():
            self.install_config.setdefault(k, v)

        if self.is_vmware_virtualization() and 'install_linux_esx' not in self.install_config:
            self.install_config['install_linux_esx'] = True

        base_path = os.path.dirname("build_install_options_all.json")
        package_list = []
        if 'packagelist_file' in self.install_config:
            package_list = PackageSelector.get_packages_to_install(self.install_config['packagelist_file'], base_path)

        if 'additional_packages' in self.install_config:
            package_list.extend(self.install_config['additional_packages'])
        self.install_config['packages'] = package_list

        if 'partitions' in self.install_config:
            partitions = self.install_config['partitions']
        else:
            partitions = modules.commons.default_partitions

        self.install_config['disk'] = modules.commons.partition_disk(self.install_config['disk'], partitions)

        if not self.iso_config_is_enabled('SKIP_NETWORK_CONFIG'):
            print("Setting up network!")
            if 'vlan_id' in self.install_config:
                print(" - with vlan")
                vlan_cfg = NetworkConfigVlan(self.install_config)
                vlan_cfg.networkconfig_using_vlanid()
            else:
                net_cfg = ConfigureNetwork(self.install_config)
                if 'dhcphostname' in self.install_config:
                    print(" - with dhcp hostname")
                    # Network autoconfiguration with a DHCP hostname
                    err, msg = ConfigureNetwork.validate_hostname(self.install_config['dhcphostname'])
                    if err:
                        raise Exception(msg)
                    # TODO implement this !
                elif 'ipaddr' not in self.install_config:
                    print(" - with auto configuration")
                    # Try to auto configure network if 'ipaddr' key is notfound
                    net_cfg._execute_modules(modules.commons.PRE_INSTALL_CONFIG_AUTO, 'm_autoconfig.py')
                else:
                    print(" - manually with static ip")
                    # Manual, network configuration
                    # Expect to have ipaddr, netmask, gateway, and namsespace_server from ks_config
                    for i in [self.install_config['ipaddr'], self.install_config['netmask'], self.install_config['gateway'], self.install_config['namespace_server']]:
                        err, msg = ConfigureNetwork.validate_ipaddr(i)
                        if err:
                            raise Exception(msg)
                    check = self._execute_modules(modules.commons.PRE_INSTALL_CONFIG)
                    if check != 0:
                        raise Exception('Failed to configure the network manually')

            if not self.iso_config_is_enabled('SKIP_NSX_CONFIG') and 'nsx_ks_url' in self.install_config:
                print("Downloding nsx config!")
                nsx_ks_cfg = NSXAplianceConfig(self.install_config)
                if not nsx_ks_cfg.download_file(self.install_config['nsx_ks_url']):
                    print("Failed to download NSX ks file!")

        if "hostname" in self.install_config:
            evalhostname = os.popen('printf ' + self.install_config["hostname"].strip(" ")).readlines()
            self.install_config['hostname'] = evalhostname[0]
        if "hostname" not in self.install_config or self.install_config['hostname'] == "":
            self.install_config['hostname'] = "photon-" + self.random_id.strip()

        # crypt the password if needed
        if self.install_config['password']['crypted']:
            self.install_config['password'] = self.install_config['password']['text']
        else:
            self.install_config['password'] = crypt.crypt(
                self.install_config['password']['text'],
                "$6$" + "".join([random.choice(
                    string.ascii_letters + string.digits) for _ in range(16)]))

    @staticmethod
    def validate_hostname(hostname):
        """A valid hostname must start with a letter"""
        error_empty = "Empty hostname or domain is not allowed"
        error_dash = "Hostname or domain should not start or end with '-'"
        error_hostname = "Hostname should start with alpha char and <= 64 chars"

        if hostname is None or not hostname:
            return False, error_empty

        fields = hostname.split('.')
        for field in fields:
            if not field:
                return False, error_empty
            if field[0] == '-' or field[-1] == '-':
                return False, error_dash

        machinename = fields[0]
        return (len(machinename) <= 64 and
                machinename[0].isalpha(), error_hostname)

    def validate_ostree_url_input(ostree_repo_url):
        if not ostree_repo_url:
            return False, "Error: Invalid input"

        exception_text = "Error: Invalid or unreachable URL"
        error_text = "Error: Repo URL not accessible"
        ret = IsoConfig.validate_http_response(ostree_repo_url, [], exception_text, error_text)
        if ret != "":
            return False, ret

        exception_text = "Error: Invalid repo - missing config"
        ret = IsoConfig.validate_http_response(
            ostree_repo_url + "/config",
            [ [".*\[core\]\s*", 1, "Error: Invalid config - 'core' group expected" ],
              ["\s*mode[ \t]*=[ \t]*archive-z2[^ \t]", 1, "Error: can't pull from repo in 'bare' mode, 'archive-z2' mode required" ] ],
            exception_text, exception_text)
        if ret != "":
            return False, ret

        exception_text = "Error: Invalid repo - missing refs"
        ret = IsoConfig.validate_http_response(ostree_repo_url + "/refs/heads", [], exception_text, exception_text)
        if ret != "":
            return False, ret

        exception_text = "Error: Invalid repo - missing objects"
        ret = IsoConfig.validate_http_response(ostree_repo_url + "/objects", [], exception_text, exception_text)
        if ret != "":
            return False, ret

        IsoConfig.g_ostree_repo_url = ostree_repo_url
        return True, None

    def validate_ostree_refs_input(ostree_repo_ref):
        if not ostree_repo_ref:
            return False, "Error: Invalid input"

        ret = IsoConfig.validate_http_response(
                #'http://10.110.19.153:8000/repo/refs/heads/' + ostree_repo_ref,
                IsoConfig.g_ostree_repo_url  + '/refs/heads/' + ostree_repo_ref,
                [ ["^\s*[0-9A-Fa-f]{64}\s*$", 1, "Error: Incomplete Refspec path, or unexpected Refspec format"] ],
                "Error: Invalid Refspec path",
                "Error: Refspec not accessible")
        if ret != "":
            return False, ret

        return True, None


    def validate_http_response( url, checks, exception_text, error_text):
        try:
            if url.startswith("https"):
                response = urlopen(url,cafile="/usr/lib/python2.7/site-packages/requests/cacert.pem")
            else:
                response = urlopen(url)

        except:
            return exception_text
        else:
            if response.getcode() != 200:
                return error_text

        html = response.read().decode('utf-8')

        for pattern, count, failed_check_text in checks:
            match = re.findall(pattern, html)
            if len(match) != count:
                return failed_check_text

        return ""

    @staticmethod
    def validate_password(text):
        """Validate password with cracklib"""
        try:
            password = cracklib.VeryFascistCheck(text)
        except ValueError as message:
            password = str(message)
        return password == text, "Error: " + password

    @staticmethod
    def generate_password_hash(password):
        """Generate hash for the password"""
        shadow_password = crypt.crypt(
            password, "$6$" + "".join(
                [random.choice(
                    string.ascii_letters + string.digits) for _ in range(16)]))
        return shadow_password

    def ui_config(self, options_file, maxy, maxx):
        """Configuration through UI"""
        # This represents the installer screen, the bool indicated if
        # I can go back to this window or not
        items, select_linux_index = self.add_ui_pages(options_file, maxy, maxx)
        index = 0
        while True:
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
                    index = 0

    @staticmethod
    def chomp(s):
        if s.endswith("\r\n"):
            return s[:-2]
        if s.endswith("\n") or s.endswith("\r"):
            return s[:-1]
        return s

    @staticmethod
    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)

    @staticmethod
    def parse_config_file(fname):
        config={}
        try:
            with open(fname, 'r') as f:
                lines = f.readlines()
        except Exception:
            return config # return empty

        for line in lines:
            line = IsoConfig.chomp(line)
            if re.match('^\s*$', line) or re.match('^#', line):
                continue
            match = re.findall('^(\w+)\s*=\s*(.+)$', line)
            if len(match) != 1:
                print("Error: invalid entry '{}' in config file '{}'. Skipping it.".format(line, fname))
                continue
            config.update(match)
        return config

    def iso_config_is_enabled(self, key):
        return self.install_config['iso_config'].get(key, '') == 'yes'

    def add_ui_pages(self, options_file, maxy, maxx):
        items = []
        license_agreement = License(maxy, maxx)

        select_disk = SelectDisk(maxy, maxx, self.install_config)
        select_partition = PartitionISO(maxy, maxx, self.install_config)
        hostname_reader = WindowStringReader(
            maxy, maxx, 10, 70,
            'hostname',
            None, # confirmation error msg if it's a confirmation text
            None, # echo char
            self.hostname_accepted_chars, # set of accepted chars
            IsoConfig.validate_hostname, # validation function of the input
            None, # post processing of the input field
            'Choose the hostname for your system', 'Hostname:', 2, self.install_config,
            self.random_hostname,
            True)
        root_password_reader = WindowStringReader(
            maxy, maxx, 10, 70,
            'password',
            None, # confirmation error msg if it's a confirmation text
            '*', # echo char
            None, # set of accepted chars
            IsoConfig.validate_password, # validation function of the input
            None,  # post processing of the input field
            'Set up root password', 'Root password:', 2, self.install_config)
        confirm_password_reader = WindowStringReader(
            maxy, maxx, 10, 70,
            'password',
            # confirmation error msg if it's a confirmation text
            "Passwords don't match, please try again.",
            '*', # echo char
            None, # set of accepted chars
            None, # validation function of the input
            IsoConfig.generate_password_hash, # post processing of the input field
            'Confirm root password', 'Confirm Root password:', 2, self.install_config)

        ostree_server_selector = OSTreeServerSelector(maxy, maxx, self.install_config)
        ostree_url_reader = OSTreeWindowStringReader(
            maxy, maxx, 10, 80,
            'ostree_repo_url',
            None, # confirmation error msg if it's a confirmation text
            None, # echo char
            None, # set of accepted chars
            IsoConfig.validate_ostree_url_input, # validation function of the input
            None, # post processing of the input field
            'Please provide the URL of OSTree repo', 'OSTree Repo URL:', 2, self.install_config,
            "http://")
        ostree_ref_reader = OSTreeWindowStringReader(
            maxy, maxx, 10, 70,
            'ostree_repo_ref',
            None, # confirmation error msg if it's a confirmation text
            None, # echo char
            None, # set of accepted chars
            IsoConfig.validate_ostree_refs_input, # validation function of the input
            None, # post processing of the input field
            'Please provide the Refspec in OSTree repo', 'OSTree Repo Refspec:', 2, self.install_config,
            "photon/3.0/x86_64/minimal")

        items.append((license_agreement.display, False))
        items.append((select_disk.display, True))
        items.append((select_partition.display, False))
        items.append((select_disk.guided_partitions, False))

        if not self.iso_config_is_enabled('SKIP_NETWORK_CONFIG'):
            net_cfg_vlan = NetworkConfigVlan(self.install_config, maxy, maxx)
            items.append((net_cfg_vlan.display_config_network, True))

            if not self.iso_config_is_enabled('SKIP_NSX_CONFIG'):
                nsx_ks_cfg = NSXAplianceConfig(self.install_config, maxy, maxx)
                items.append((nsx_ks_cfg.display, True))

        json_wrapper_option_list = JsonWrapper(options_file)
        options = json_wrapper_option_list.read()
        options['base_path'] = os.path.dirname(options_file)

        if self.iso_config_is_enabled('SKIP_OSTREE'):
            options['ostree_host']['visible'] = False

        package_selector = PackageSelector(maxy, maxx, self.install_config, options)
        items.append((package_selector.display, True))

        select_linux_index = -1
        if self.is_vmware_virtualization():
            linux_selector = LinuxSelector(maxy, maxx, self.install_config)
            items.append((linux_selector.display, True))
            select_linux_index = items.index((linux_selector.display, True))
        items.append((hostname_reader.get_user_string, True))
        items.append((root_password_reader.get_user_string, True))
        items.append((confirm_password_reader.get_user_string, False))
        items.append((ostree_server_selector.display, True))
        items.append((ostree_url_reader.get_user_string, True))
        items.append((ostree_ref_reader.get_user_string, True))

        return items, select_linux_index
