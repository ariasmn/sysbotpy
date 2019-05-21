import socket
import socketserver
import json
import host_administration as hostadmin

SERVER_ADDR = "192.168.1.60"

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
                hostadmin.shutdownHost()
            elif command == "restart":
                hostadmin.restartHost()
            else:
                print ("Can't recognize command")

class ThreadedServer (socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

local_server = ThreadedServer(('', 1337), handler)
local_server.serve_forever()