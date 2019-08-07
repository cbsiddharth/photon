import os
import random
import commons
import subprocess

install_phase = commons.PRE_INSTALL_CONFIG_BACKUP
enabled = True

def execute(config, root):
    mkcmd = "mkdir /tmp/orig"
    test = subprocess.Popen(mkcmd, stdout=subprocess.DEVNULL, shell=True)
    test.wait()
    cpcmd = "cp /etc/systemd/network/* /tmp/orig/"
    test = subprocess.Popen(cpcmd, stdout=subprocess.DEVNULL, shell=True)
    test.wait()

    with open('out.txt', 'a+') as f:
        print(" In Backup file !!",file=f)
    return 0
