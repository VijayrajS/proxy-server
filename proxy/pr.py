import socketserver, threading
from time import sleep
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler

PORT = 20100

class Proxy(SimpleHTTPRequestHandler):
    # Get request handler (add caching code in this function)
    def do_GET(self):
        client_addr = self.client_address
        print(">> PROXY_SERVER : ", client_addr)
        print(" PROXY_SERVER : GET : Handling Client ", str(self.client_address))
        print("Thread Name:{}".format(threading.current_thread().name))

        self.copyfile(urlopen(self.path), self.wfile)
        print("SUCCESS")


    def do_POST(self):
        client_addr = self.client_address
        print(">> PROXY_SERVER : ", client_addr)
        print(" PROXY_SERVER : Handling Client ", str(self.client_address))

        self.copyfile(urlopen(self.path), self.wfile)
        print("SUCCESS")


class MasterControlThread(threading.Thread):
    def __init__(self, port=20100):
        threading.Thread.__init__(self)
        self.port = port
        self.lock = threading.RLock()

    def run(self):
        try:
            print("Serving on port", self.port)
            self.server = socketserver.ThreadingTCPServer(('', PORT), Proxy)
            # Note: Five seconds timeout instead of a minute, for testing.
            self.thread = threading.Thread(target=self.server.serve_forever)
            self.thread.start()
        except KeyboardInterrupt:
            # Tell the server it's time to shut down
            self.lock.acquire()
            self.QuitFlag = 1
            self.lock.release()
            # print "Waiting for server to shut down (could take several seconds)..."
            self.thread.join()
            print("Exiting now.")

if __name__ == '__main__':
    mct = MasterControlThread()
    mct.start()
    mct.join()

# if __name__ == "__main__":
#     try:
#         print(">> PROXY_SERVER : Proxy server running")
#         httpd = socketserver.ThreadingTCPServer(('', PORT), Proxy)
#         print(">> PROXY_SERVER : Serving at port", PORT)
#         httpd.serve_forever()

#     except KeyboardInterrupt:
#         print("\n>> PROXY_SERVER : __SIGINT__ detected")
#         print(">> PROXY_SERVER : << Shutting down >>")
#         httpd.shutdown()

#     except Exception as _exc:
#         print("\n>> PROXY_SERVER : _Exception_\n",_exc)
#         print(">> PROXY_SERVER : << Shutting down >>")
#         httpd.shutdown()

