import os
import random
import commons
import subprocess
from glob import glob

install_phase = commons.PRE_INSTALL_CONFIG_VLAN
enabled = True

def execute(config, root):
    for filename in glob("/etc/systemd/network/*"):
        os.remove(filename)
    cpcmd = "cp /tmp/orig/* /etc/systemd/network/"
    test = subprocess.Popen(cpcmd, stdout=subprocess.DEVNULL, shell=True)
    test.wait()

    if 'vlan_id' in config:
        ipcmd = "ip link delete eth0."+str(config['vlan_id'])
        test = subprocess.Popen(ipcmd, stdout=subprocess.DEVNULL, shell=True)
        test.wait()
         
    with open('out.txt', 'a+') as f:
        print(" In Vlan before file !!",file=f)
    return 0
