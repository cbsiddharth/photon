import os
import random
import commons

install_phase = commons.POST_INSTALL
enabled = True

def execute(config, root):
    pass
    #hostname = config['dhcphostname']

    #hostname_file = os.path.join(root, 'etc/systemd/network/*-dhcp-en.network')
    #hosts_file    = os.path.join(root, 'etc/hosts')
    #dhcp_host = "\n[DHCP]\nSendHostname=True\nHostname="+str(hostname)
    #with open(hostname_file, 'a+b') as outfile:
    #    outfile.write(dhcp_host.encode())

    #pattern = r'(127\.0\.0\.1)(\s+)(localhost)\s*\Z'
    #replace = r'\1\2\3\n\1\2' + hostname
    #commons.replace_string_in_file(hosts_file, pattern, replace)
