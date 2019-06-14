# SysBotpy
A Telegram Bot implementation for basic system monitoring and administration.
Final project for my AD/HND in Software Engineering.

## SYNOPSIS
It's an easy distributed application based in a client-server model, using the [Telegram Bot API](https://core.telegram.org/bots/api). You can get basic info like local IP, OS, logged user, and also shutdown/restart the host via a private Telegram Bot. It uses TCP socket programming for local network communication between the server and the hosts.

This is not a well-tested, neither a stable implementation, and it's only intended for home/personal use, since it was made mostly to learn about Python, socket programming, freezing tools and running Python scripts as services in Windows/Linux.

## RESOURCES

 - [Python 3.x](https://github.com/python/cpython)
 - [pip](https://github.com/pypa/pip)
 - [psutil](https://github.com/giampaolo/psutil)
 - [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
 
 Also, I used [Nuitka](https://github.com/Nuitka/Nuitka) to compile my client-side script for an easy cross-platform deployment and [SrvStart](https://github.com/rozanski/srvstart) for the service implementation in Windows.

## HOW IT WORKS?
The project uses Telegram as the "front-end". It relies on the usage of Telegram Bots.

![enter image description here](https://user-images.githubusercontent.com/33121576/59517396-d1bb7100-8ec3-11e9-9529-8416d338a797.png)

## INSTALLATION
For the installation, you have the choice to run the script normally with Python 3 and installing the needed libraries using pip in both clients and the server:

    pip install -r requirements.txt
It's up to you if you use [virtualenv](https://github.com/pypa/virtualenv).

Also, the implementation has been tested in **Nuitka**, and it's working with the client script without any problems (as far as I can tell). To compile it, I used the option **standalone**, so the host doesn't need to have any Python interpreter installed:

    python -m nuitka --standalone --follow-imports main.py
Keep in mind that you need to compile in the OS you are willing to run the application in. Also, a C Compiler is needed for Windows, but you can find all the information you need in the [Nuitka user manual page.](https://nuitka.net/doc/user-manual.html)

Also, in both client and server you can find a **config.ini** file. In the client, you can set the port to use and the server IP address (better if you do it using a firewall). In the server, you can set the port, your Telegram Bot private token and the ID of the Telegram users that are whitelisted (only those whitelisted users are capable of using the bot). 

In order to create your Telegram Bot, you need to use [BotFather](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
