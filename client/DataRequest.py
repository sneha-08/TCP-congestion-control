from socket import *
import time
import sys

PAYLOAD_SIZE = 4096
MEGA = 10**6

if len(sys.argv) is not 3:
    print("Wrong format. Enter: python DataRequest.py <ip> <port>")
    exit()

serverName = sys.argv[1]
serverPort = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))


payload = bytearray(PAYLOAD_SIZE)

while 1:
    # send data
    clientSocket.send(payload)

clientSocket.close()