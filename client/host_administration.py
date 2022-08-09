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


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip_addr = s.getsockname()[0]
    except BaseException:
        ip_addr = '127.0.0.1'
    finally:
        s.close()
    return ip_addr


def send_system_info():
    if platform.system() == 'Linux':
        info = Host(platform.linux_distribution(), socket.gethostname(),
                    getpass.getuser(), get_ip(), procadmin.send_processes())
        # formatting. linux_distribution() returns a list of string, join them
        # with an space between them.
        info.os = " ".join(info.os)
    else:
        info = Host(platform.platform(), socket.gethostname(),
                    getpass.getuser(), get_ip(), procadmin.send_processes())
    return info


def shutdown_host():
    if platform.system() == "Windows":
        os.system('shutdown /p /f')
    else:
        os.system('systemctl poweroff')


def restart_host():
    if platform.system() == "Windows":
        os.system("shutdown /r /t 1")
    else:
        os.system('systemctl reboot')
