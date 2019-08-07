import os
import random
import commons
import subprocess
from glob import glob

install_phase = commons.PRE_INSTALL_CONFIG_AUTO
enabled = True


def execute(config, root):
    for filename in glob("/etc/systemd/network/*"):
        os.remove(filename)
    cpcmd = "cp /tmp/orig/*-dhcp-en.network /etc/systemd/network/"
    test = subprocess.Popen(cpcmd, stdout=subprocess.DEVNULL, shell=True)
    test.wait()

    cmd3 = "systemctl restart systemd-networkd"
    test = subprocess.Popen(cmd3, stdout=subprocess.DEVNULL, shell=True)
    test.wait()
    return 0
