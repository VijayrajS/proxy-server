import sys
import time
import re
import threading
from socket import *

server_port = 20100


class Server:
    def __init__(self):
        try:
            self.server_socket = socket(AF_INET, SOCK_STREAM)  # Create a TCP socket
            self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Re-use the socket
        except error as e:
            message = 'Unable to create/re-use the socket. Error: %s' % e
            print(message)
        # bind the socket to a public/local host, and a port
        self.server_socket.bind(('', server_port))
        # allowing up to 10 client connections
        self.server_socket.listen(10)
        message = "Host Name: Localhost and Host address: 127.0.0.1 and Host port: " + \
            str(server_port) + "\n"
        print(message)
        print "Server is ready to listen for clients"


if __name__ == "__main__":
    # creating the instance of the server class
    server = Server()
    # calling the listen to Client call
    server.listen_to_client()
