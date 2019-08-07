#    Author: Ajay Kaher <akaher@vmware.com>

import sys
import time
import requests
import shutil
from window import Window
from windowstringreader import WindowStringReader
from actionresult import ActionResult

class NSXAplianceConfig(object):

    def __init__(self, install_config, maxy=0, maxx=0):
        self.install_config = install_config
        self.alpha_chars = list(range(65, 91))
        self.alpha_chars.extend(range(97, 123))
        self.url_accepted_chars = self.alpha_chars
        self.maxy = maxy
        self.maxx = maxx

        # Adding the numeric chars
        self.url_accepted_chars.extend(range(48, 58))
        # Adding the ., : and -
        self.url_accepted_chars.extend([ord('.'), ord('-'), ord('/'), ord('_'), ord(':')])

        self.random_url = "https://jpeg.org/images/jpeg-home.jpg"

    def download_file(self, url):
        try:
            r = requests.get(url, verify=False, stream=True, timeout=5.0)
        except Exception:
            return False
        r.raw.decode_content = True
        with open("/installer/nsx_ks.cfg", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        return True

    def display(self, params):
        status_window = None
        while True:
            nsx_url_reader = WindowStringReader(
                self.maxy, self.maxx, 18, 78,
                'nsx_ks_url',
                None, # confirmation error msg if it's a confirmation text
                None, # echo char
                self.url_accepted_chars, # set of accepted chars
                None, # validation function of the input
                None, # post processing of the input field
                '[!] Configure NSX appliance using kickstart', 'This is used to automate the provisioning of an NSX appliance using a\nconfig file composed of CLI commands. By default, this is blank\n(lease blank if not used). Please note that this question is\ngenerally specified as a boot parameter during the initial install of\na NSX appliance. \n\nPlease enter the url for the NSX kickstart config file:',
                10,
                self.install_config,
                self.random_url,
                True)

            result = nsx_url_reader.get_user_string(None)
            if not result.success:
                return result

            if status_window is None:
                status_window = Window(10,70, self.maxy, self.maxx, 'Installing Photon', False)
                status_window.addstr(1, 0, 'Downloading NSX kickstart config file...')
            status_window.show_window()

            status = self.download_file(self.install_config['nsx_ks_url'])

            if status is True:
                return ActionResult(True, None)

            status_window.adderror('Oops, download failed. Press any key to go back...')
            status_window.content_window().getch()
            status_window.clearerror()
            status_window.hide_window()
            continue
