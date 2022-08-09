from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import re
import socket
import sys
import json
import logging
import configparser
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

actual_path = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read(os.path.join(actual_path, 'config.ini'))

PORT = config.getint('CONFIG', 'PORT')
WHITELIST = json.loads(config.get('WHITELIST', 'id'))
TOKEN = config.get('CONFIG', 'TOKEN')


def check_permission(chat_id):
    if chat_id not in WHITELIST:
        return False
    else:
        return True


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def is_up(addr):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # timeout in order to stop blocking socket on each iteration
    s.settimeout(0.01)
    if not s.connect_ex((addr, PORT)):
        s.close()
        return 1
    else:
        s.close()


def run(subnet):
    up_hosts = []
    for ip in range(1, 256):
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
            print(socket.error)
        s.connect((host, PORT))
        request = ("info").encode()
        try:
            s.sendall(request)
        except socket.error:
            print('Send failed')
            sys.exit()
        reply = (s.recv(4096)).decode()
        hosts_json.append(reply)
    return hosts_json


def shutdown_host(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print(socket.error)
    s.connect((host, PORT))
    request = ("shutdown").encode()
    try:
        s.sendall(request)
    except socket.error:
        print('Send failed')
        sys.exit()


def restart_host(host):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print(socket.error)
    s.connect((host, PORT))
    request = ("restart").encode()
    try:
        s.sendall(request)
    except socket.error:
        print('Send failed')
        sys.exit()


def all(bot, update):
    chat_id = update.message.chat_id

    if not check_permission(chat_id):
        bot.send_message(
            chat_id=chat_id,
            text="No tienes permitido ejecutar comandos en este bot. Contacte con el administrador")
        return

    data = get_data(run('192.168.1.'))

    if not data:
        bot.send_message(chat_id=chat_id, text="No hay hosts vivos")
        return
    for each_host in data:
        each_host = json.loads(each_host)

        keyboard = [
            [
                InlineKeyboardButton(
                    "Apagar",
                    callback_data=each_host['ip_addr'] +
                    ",shutdown"),
                InlineKeyboardButton(
                    "Reiniciar",
                    callback_data=each_host['ip_addr'] +
                    ",restart")]]

        message = ("- Sistema operativo : " + each_host['os'] +
                   "\n- Nombre de host : " + each_host['hostname'] +
                   "\n- Usuario logeado : " + each_host['user_logged'] +
                   "\n- IP local : " + each_host['ip_addr'])

        if "Windows" in each_host['os']:
            photo = open("assets/windows.png", "rb")
        else:
            photo = open("assets/linux.png", "rb")

        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_photo(chat_id=chat_id, photo=photo,
                       caption=message, reply_markup=reply_markup)


def inline_button_callback(bot, update):
    query = update.callback_query

    what_to_do = query.data.split(',')[1]
    host_ip = query.data.split(',')[0]

    if what_to_do == "shutdown":
        shutdown_host(host_ip)
        bot.delete_message(chat_id=query.message.chat_id,
                           message_id=query.message.message_id)
    elif what_to_do == "restart":
        restart_host(host_ip)
        bot.delete_message(chat_id=query.message.chat_id,
                           message_id=query.message.message_id)
        #bot.edit_message_caption(chat_id=query.message.chat_id, message_id=query.message.message_id, caption="Host reiniciado")
    else:
        return


def start(bot, update):
    chat_id = update.message.chat_id

    if not check_permission(chat_id):
        bot.send_message(
            chat_id=chat_id,
            text="No tienes permitido ejecutar comandos en este bot. Contacte con el administrador")
        return

    bot.send_message(
        chat_id=chat_id, text=(
            "Bot de Telegram para la administración de sistemas\n"
            "Realizado por Ismael Arias para CFGS de DAM\n"
            "IES Virgen del Carmen\n\n"
            "Puede ver los comandos disponibles haciendo click en el icono de '/' en tu cliente de Telegram"))


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('all', all))
    dp.add_handler(CallbackQueryHandler(inline_button_callback))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
