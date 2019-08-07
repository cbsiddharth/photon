import os
import random
import commons
import subprocess
from glob import glob

install_phase = commons.POST_INSTALL
enabled = True

def execute(config, root):

    network_file = os.path.join(root, 'etc/systemd/network/*')
    network_file_path = os.path.join(root, 'etc/systemd/network/')
    for filename in glob(network_file):
        os.remove(filename)
    cpcmd = "cp /etc/systemd/network/* "+str(network_file_path)
    test = subprocess.Popen(cpcmd, stdout=subprocess.DEVNULL, shell=True)
    test.wait()
    chmodcmd = "chmod 0644 "+str(network_file)
    test = subprocess.Popen(chmodcmd, stdout=subprocess.DEVNULL, shell=True)
    test.wait()
