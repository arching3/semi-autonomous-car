import socket
import sys
from time import sleep


#Command form = =COMMAND STRENGTH+


sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = "192.168.137.146"  # ESP32 IP in local network
port = 80 # ESP32 Server Port
sock.connect((host, port))
print("Connect Success")
while True:
    a = input()
    sock.sendall(a.encode())
    if(a == "break"):
        break


sleep(1)
sock.close()
