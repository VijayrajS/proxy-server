import socketserver, threading
from time import sleep
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler

PORT = 20100

class Proxy(SimpleHTTPRequestHandler):
    # Get request handler (add caching code in this function)
    def do_GET(self):
        try:
            client_addr = self.client_address
            print(">> PROXY_SERVER : ", client_addr)
            print(" PROXY_SERVER : GET : Handling Client ", str(self.client_address))
            print("Thread Name:{}".format(threading.current_thread().name))

            self.copyfile(urlopen(self.path), self.wfile)
            print("SUCCESS")
        except:
            print("\n>> PROXY_SERVER : __SIGINT__ detected")
            print(">> PROXY_SERVER : << Shutting down >>")
            exit()
            return

    def do_POST(self):
        client_addr = self.client_address
        print(">> PROXY_SERVER : ", client_addr)
        print(" PROXY_SERVER : Handling Client ", str(self.client_address))

        self.copyfile(urlopen(self.path), self.wfile)
        print("SUCCESS")


if __name__ == "__main__":
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(('', PORT), Proxy)
    try:
        print(">> PROXY_SERVER : Proxy server running")
        print(">> PROXY_SERVER : Serving at port", PORT)
        httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n>> PROXY_SERVER : __SIGINT__ detected")
        print(">> PROXY_SERVER : << Shutting down >>")
        httpd.server_close()
        httpd.shutdown()

    except Exception as _exc:
        print("\n>> PROXY_SERVER : _Exception_\n",_exc)
        print(">> PROXY_SERVER : << Shutting down >>")
        httpd.server_close()
        httpd.shutdown()

