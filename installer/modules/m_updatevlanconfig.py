import os
import random
import commons
import subprocess
from glob import glob

install_phase = commons.POST_INSTALL
enabled = True


def execute(config, root):
    if "nsx_ks_url" in config:
        file_path = os.path.join(root, 'opt')
        cmd = "mkdir "+str(file_path)+"; mkdir "+str(file_path)+"/vmware; mkdir "+str(file_path)+"/vmware/tmp"
        test = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, shell=True)
        test.wait()
        fpath = os.path.join(root, 'opt/vmware/tmp')
        cpcmd = "cp /installer/nsx_ks.cfg "+str(fpath)
        test = subprocess.Popen(cpcmd, stdout=subprocess.DEVNULL, shell=True)
        test.wait()
    return 0
