import socketserver, threading
from time import sleep
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler

PORT = 20101

class Proxy(SimpleHTTPRequestHandler):
    def handle(self):
        print(" PROXY_SERVER : Handling Client ", str(self.client_address))
        self.data = self.request.recv(1024).strip()
        print(self.data)


class ProxyServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, handler_class = Proxy):
        print('__init__')
        socketserver.TCPServer.__init__(self, server_address, handler_class)
        return

    def server_activate(self):
        # print('server_activate')
        socketserver.TCPServer.server_activate(self)
        return

    def handle_request(self):
        return socketserver.TCPServer.handle_request(self)

    def verify_request(self, request, client_address):
        # print('verify_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.verify_request(self, request, client_address)

    def process_request(self, request, client_address):
        # print('process_request(%s, %s)', request, client_address)
        return socketserver.TCPServer.process_request(self, request, client_address)

if __name__ == "__main__":
    try:
        print(">> PROXY_SERVER : Proxy server running")
        httpd = ProxyServer(('', PORT), Proxy)

        print(">> PROXY_SERVER : Serving at port", PORT)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=httpd.serve_forever)

        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        try:
            while True:
                sleep(1)
        except:
            pass

    except KeyboardInterrupt:
        print("\n>> PROXY_SERVER : __SIGINT__ detected")
        print(">> PROXY_SERVER : << Shutting down >>")
        httpd.shutdown()

    except Exception as _exc:
        print("\n>> PROXY_SERVER : _Exception_\n",_exc)
        print(">> PROXY_SERVER : << Shutting down >>")
        httpd.shutdown()

