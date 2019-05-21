import socket
import sys
import json

PORT = 1337

def is_up(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.01)    ## timeout in order to stop blocking socket on each iteration
    if not s.connect_ex((addr,PORT)):
        s.close()                  
        return 1
    else:
        s.close()

def run(subnet):
    up_hosts = []
    for ip in range(1,256):
        addr = str(subnet) + str(ip)
        if is_up(addr):
            up_hosts.append(addr)
    return up_hosts

def get_data(hosts):
    for host in hosts:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            sys.exit()
        s.connect((host , PORT))
        request = ("info").encode()
        try:
            s.sendall(request)
        except socket.error:
            print ('Send failed')
            sys.exit()
        reply = (s.recv(4096)).decode()
        print (reply)

hosts = run("192.168.1.")
get_data(hosts)