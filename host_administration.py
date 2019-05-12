import platform
import getpass
import socket
import os
import process_administration as procadmin

class Host:

    def __init__(self, os, hostname, user_logged, ip_addr, processes):
        self.os = os
        self.hostname = hostname
        self.user_logged = user_logged
        self.ip_addr = ip_addr
        self.processes = processes

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def sendSystemInfo():
    if platform.system() == 'Linux':
        info = Host(platform.linux_distribution(), socket.gethostname(), getpass.getuser(), getIP(), procadmin.sendProcesses())
        info.os = " ".join(info.os) #formatting. linux_distribution() returns a list of string, join them with an space between them.
    else:
        info = Host(platform.platform(), socket.gethostname(), getpass.getuser(), getIP(), procadmin.sendProcesses())
    return info

def shutdownHost():
    if platform.system() == "Windows":
        os.system('shutdown /p /f')
    else:
        os.system('systemctl poweroff')

def restartHost():
    if platform.system() == "Windows":
        os.system("shutdown /r /t 1")
    else:
        os.system('systemctl restart')


