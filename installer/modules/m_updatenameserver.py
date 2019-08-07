import os
import random
import commons
import subprocess

install_phase = commons.PRE_INSTALL_CONFIG
enabled = True

def read_ip(ip_param):
    newip = ""
    for ch in ip_param:
        if (ch >= '0' and ch <= '9') or ch == '.': 
            newip += ch
    return newip


def ip_status():
    getipcmd="ifconfig eth0 | grep \'inet\ addr\' | cut -d: -f2 | cut -d\' \' -f1"
    ip = subprocess.Popen(getipcmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    newip = read_ip(str(ip))
    with open('out.txt', 'a+') as f:
        print(newip,file=f)
    cmd="ifconfig eth0"
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]
    with open('out.txt', 'a+') as f:
        print(result,file=f)
    if str(newip) in str(result):
        with open('out.txt', 'a+') as f:
            print("Successfully name server done !!",file=f)
            return 0
    else:
        return 1

def execute(config, root):
    ipaddr = config['ipaddr']
    gateway = config['gateway']
    namespace_server = config['namespace_server']
    input = namespace_server.split(" ")

    with open('out.txt', 'a+') as f:
        print(" In Nameserver file !!",file=f)
    match_string = "nameserver"
    insert_string = ""
    index=0
    for i in range(len(input)):
        insert_string += "\nnameserver "+str(input[i])
    file_path = os.path.join(root, 'etc/resolv.conf')
    with open('out.txt', 'a+') as f:
        print(file_path,file=f)
        print(insert_string,file=f)
    newcontents = ""
    with open(file_path, 'r+') as fd:
        contents = fd.readlines()
        #with open('out.txt', 'a+') as f:
        #    print("\ncontent::::::\n",file=f)
        #    print(contents,file=f)
        if contents:
            for index, line in enumerate(contents):
                #with open('out.txt', 'a+') as f:
                #    print("\nindex=%d"%index,file=f)
                #    print("\nline="+str(line),file=f)
                if match_string in line:
                    contents.insert(index-1,insert_string)
                    break
        fd.seek(0)
        #with open('out.txt', 'a+') as f:
        #    print("\nNew content::::::\n",file=f)
        #    print(contents,file=f)
        newcontents = contents
        fd.writelines(contents)
        fd.flush()
    with open('out.txt', 'a+') as f:
        print("\nNewer content::::::\n",file=f)
        print(newcontents,file=f)
    #mvcmd = "mv /etc/resolv.conf /root/"
    #test = subprocess.Popen(mvcmd, stdout=subprocess.DEVNULL, shell=True)
    #test.wait()
    #with open(file_path, 'w+') as fd:
    #    fd.writelines(newcontents)

    #cmd3 = "systemctl restart systemd-networkd"
    #test = subprocess.Popen(cmd3, stdout=subprocess.DEVNULL, shell=True)
    #test.wait()

    check_ip = ip_status() 
    return check_ip
