import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.1", 1337))
server_socket.listen(15)

print ("Testing para proyecto\n")

def devolverAlgo(sc):
    sc.send("Funcionando\n".encode('utf8'))
    sc.close()

while True:
    sc, addr = server_socket.accept()
    print ("IP del cliente: ", addr)
    
    received = (sc.recv(48000)).decode('utf8')

    if received.strip() == "algo":
        devolverAlgo(sc)