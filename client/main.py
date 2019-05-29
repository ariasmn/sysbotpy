import socket
import socketserver
import json
import host_administration as hostadmin
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

SERVER_ADDR = config.get('CONFIG', 'SERVER_ADDR')
PORT = config.getint('CONFIG', 'PORT')

class handler (socketserver.BaseRequestHandler):
    #need to be overriden. You will pass this class as an argument in the ThreadedServer declaration
    def handle(self):
        if self.client_address[0] != SERVER_ADDR:
            self.request.sendall(str.encode("You are not allowed to connect through this port\n"))
            self.request.close()
        else:
            command = self.request.recv(1024).decode('utf-8').strip()
            if command == "info":
                info = hostadmin.sendSystemInfo()
                # using default lambda ... you are telling the serializer to convert to an object if the python type is not primitive. Needed for processes nested object.
                json_object = json.dumps(info, default = lambda x: x.__dict__)
                self.request.sendall(json_object.encode())
            elif command == "shutdown":
                success = hostadmin.shutdownHost()
                self.request.sendall(success.encode())
            elif command == "restart":
                hostadmin.restartHost()
            else:
                return

class ThreadedServer (socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

local_server = ThreadedServer(('', PORT), handler)
local_server.serve_forever()