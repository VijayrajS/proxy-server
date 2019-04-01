import socketserver, threading
from time import sleep
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler

PORT = 20100

class Proxy(SimpleHTTPRequestHandler):
    # def do_GET(self):
    #     print(">> PROXY_SERVER : ", self.client_address)
        
    #     client_addr = self.client_address
    #     # client_addr is a tuple consisting of the ip address and socket number
    #     # of the client. Using this, write a condition for allowing requests only
    #     # from appropriate socket numbers
        
    #     self.copyfile(urlopen(self.path), self.wfile)
    #     print("SUCCESS")
    def handle(self):

        print(" PROXY_SERVER : Handling Client ", str(self.client_address))


if __name__ == "__main__":
    try:
        print(">> PROXY_SERVER : Proxy server running")
        httpd = socketserver.ThreadingTCPServer(('', PORT), Proxy)
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

