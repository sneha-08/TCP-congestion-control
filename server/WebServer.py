#Import socket module
from socket import *
import sys 
import os
import time, datetime
import threading
import csv


LABEL_X = 'Time'
LABEL_Y = '[Mb/s]'

is_server_running = True
number_of_connections = 0

PAYLOAD_SIZE = 4096 #bytes
TIME_WINDOW = 2 #seconds
MEGA = 10**6

class PayloadSize:
    def __init__(self, size):
        self.size = size

class Timer (threading.Thread):
    def __init__(self, delay, payloadSize):
        threading.Thread.__init__(self)
        self.delay = delay
        self.payloadSize = payloadSize
      
    def run(self):
        global is_server_running
        global number_of_connections
        
        while os.path.exists("log%s.csv" % number_of_connections):
            number_of_connections += 1

        with open('log%s.csv' % number_of_connections, 'w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"')
            writer.writerow([LABEL_X, LABEL_Y])
            while is_server_running:
                initialBufferSize = self.payloadSize.size
                time.sleep(self.delay)
                afterBufferSize = self.payloadSize.size

                amountOfData = afterBufferSize - initialBufferSize
                megaBitsAmountOfData = (amountOfData*8)/(10**6)
                transferRate = megaBitsAmountOfData/self.delay
                
                writer.writerow([datetime.datetime.now().isoformat(), transferRate])
                print('Transfer rate: ', transferRate, 'Mbits/s')
                file.flush()

            file.close()
class ConnectionHandler(threading.Thread):
    def __init__(self, newConnectionSocket, addr):
        threading.Thread.__init__(self)
        self.socket = newConnectionSocket
        self.id = addr[1] # Use the client port as a thread id.

    def run(self):
        global is_server_running
        payloadSize = PayloadSize(0)
        timer = Timer(TIME_WINDOW, payloadSize)
        timer.start()
        while is_server_running:
            payload = self.socket.recv(PAYLOAD_SIZE)
            payloadSize.size = payloadSize.size + sys.getsizeof(payload)

        self.socket.close()
        print("connection aborted!")

try:
    if len(sys.argv) is not 2:
        print("Wrong format. Enter: python WebServer.py <port>")
        exit()

    # Create a TCP server socket
    # (AF_INET is used for IPv4 protocols)
    # (SOCK_STREAM is used for TCP)

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverPort = int(sys.argv[1])

    # binds the socket to given port.
    serverSocket.bind(('', serverPort))
    # starts to listen for SYNACK 
    serverSocket.listen(5)
    print('The Server is ready to receive')

    while True:
        # Accepts new connections creating connection sockets 
        connectionSocket, addr = serverSocket.accept()
        
        # create new thread to handler different connections
        connectionHandler = ConnectionHandler(connectionSocket, addr)
        connectionHandler.start()

except KeyboardInterrupt:
    is_server_running = False
    serverSocket.close()
    print("Server stopped")


