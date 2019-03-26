import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.request import urlopen

PORT = 20100

class Proxy(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(">> PROXY_SERVER : ", self.client_address)
        
        client_addr = self.client_address
        # client_addr is a tuple consisting of the ip address and socket number
        # of the client. Using this, write a condition for allowing requests only
        # from appropriate socket numbers
        
        self.copyfile(urlopen(self.path), self.wfile)
        print("SUCCESS")

if __name__ == "__main__":
    try:
        print(">> PROXY_SERVER : Proxy server running")
        httpd = socketserver.ThreadingTCPServer(('', PORT), Proxy)
        print(">> PROXY_SERVER : Serving at port", PORT)
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n>> PROXY_SERVER : __SIGINT__ detected")
        print(">> PROXY_SERVER : << Shutting down >>")
        httpd.shutdown()

    except Exception as _exc:
        print("\n>> PROXY_SERVER : _Exception_\n",_exc)
        print(">> PROXY_SERVER : << Shutting down >>")
        httpd.shutdown()

