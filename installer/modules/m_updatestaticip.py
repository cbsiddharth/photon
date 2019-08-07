import os
import random
import commons
import subprocess
from glob import glob

install_phase = commons.PRE_INSTALL_CONFIG
enabled = True

def netmask_to_cidr(netmask):
    '''
    :param netmask: netmask ip addr (eg: 255.255.255.0)
    :return: equivalent cidr number to given netmask ip (eg: 24)
    '''
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])

def execute(config, root):
    ip = config['ipaddr']
    if '/' not in config['ipaddr'] and 'netmask' in config:
        ip = ip + '/' + str(netmask_to_cidr(config['netmask']))

    gateway = config['gateway']
    namespace_server = config['namespace_server']
    for filename in glob("/etc/systemd/network/*"):
        os.remove(filename)

    net_cfg = "[Match]\nName=eth0\n\n[Network]\nAddress=" + str(ip) + "\nGateway=" + str(gateway)
    net_cfg_file = os.path.join(root, 'etc/systemd/network/99-static-en.network')
    with open(net_cfg_file, 'wb') as outfile:
        outfile.write(net_cfg.encode(encoding='UTF-8',errors='strict'))

    cmd3 = "systemctl restart systemd-networkd"
    test = subprocess.Popen(cmd3, stdout=subprocess.DEVNULL, shell=True)
    test.wait()
