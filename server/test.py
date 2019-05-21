from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
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
    hosts_json = []
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
        hosts_json.append(reply)
    return hosts_json

def bop(bot, update):
    data = get_data(run('192.168.1.'))
    for each_host in data:
        each_host = json.loads(each_host)
        chat_id = update.message.chat_id
        bot.send_message(chat_id=chat_id, text=each_host['os'])

def main():
    updater = Updater('812262356:AAF1nhoDeCKaZzGax_wpFSuUsLD2c-1gGB0')
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

