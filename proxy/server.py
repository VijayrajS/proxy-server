import socketserver, threading
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler

PORT = 20100

fd = open('blacklist.txt')
blacklist = []

for line in fd.readlines():
    temp = line.strip('\n').split(':')
    if temp[0] == 'localhost':
        temp[0] = '127.0.0.1'

    blacklist.append(temp)

class Proxy(SimpleHTTPRequestHandler):
    # Get request handler (add caching code in this function)
    def do_GET(self):
        try:
            client_addr = self.client_address

            # if client_addr[2] in range(20000, 20100):
            print(">> PROXY_SERVER : ", client_addr)
            print(">> PROXY_SERVER : GET : Handling Client ", str(self.client_address))
            print(">> PROXY_SERVER : Thread Name:{}".format(threading.current_thread().name))

            dest_ip = self.path.strip("http://").split(':')
            print(dest_ip)

            print(self.requestline) # ignore

            if int(dest_ip[1]) not in range(20000,20201):
                print(">> PROXY_SERVER : Invalid request")
                threading.current_thread().join
                exit()


            if dest_ip in blacklist:
                # if no auth:
               print(">> PROXY_SERVER : Invalid request")
               exit()

            self.copyfile(urlopen(self.path), self.wfile)
            print(">> PROXY_SERVER : SUCCESS")

            # else:
            #    print(">> PROXY_SERVER : Invalid request")
            #    exit()

        except:
            threading.current_thread().join
            exit()

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
        httpd.shutdown()
        exit()

    except Exception as _exc:
        print("\n>> PROXY_SERVER : _Exception_\n",_exc)
        print(">> PROXY_SERVER : << Shutting down >>")
        httpd.shutdown()
        exit()


