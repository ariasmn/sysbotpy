from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import re
import socket
import sys
import json
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

PORT = 1337


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

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
            print (socket.error)
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

def shutdown_host (host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print (socket.error)
    s.connect((host, PORT))
    request = ("shutdown").encode()
    try:
        s.sendall(request)
    except socket.error:
        print ('Send failed')
        sys.exit()

def all(bot, update):
    data = get_data(run('192.168.1.'))
    for each_host in data:
        each_host = json.loads(each_host)

        keyboard = [[InlineKeyboardButton("Apagar", callback_data=each_host['ip_addr'] + ",shutdown"),
                    InlineKeyboardButton("Reiniciar", callback_data=each_host['ip_addr'] + ",restart")]]

        
        chat_id = update.message.chat_id
        message = ("- *Sistema operativo* : " + each_host['os'] + 
            "\n- *Nombre de host* : " + each_host['hostname'] + 
            "\n- *Usuario logeado* : " + each_host['user_logged'] +
            "\n- *IP local* : " + each_host['ip_addr'])

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown", reply_markup = reply_markup)

def inline_button_callback(bot, update):
    query = update.callback_query
    """ bot.send_message(text="Selected option: {}".format(query.data),
                    chat_id=query.message.chat_id,
                    message_id=query.message.message_id) """
    
    what_to_do = query.data.split(',')[1]
    host_ip = query.data.split(',')[0]
    if what_to_do == "shutdown":
        shutdown_host(host_ip)
    elif what_to_do == "restart":
        print ("restart")
    else:
        print ("something went wrong")
    #print (query.data.split(',')[0])


def main():
    updater = Updater('812262356:AAF1nhoDeCKaZzGax_wpFSuUsLD2c-1gGB0')
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('all',all))
    dp.add_handler(CallbackQueryHandler(inline_button_callback))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

