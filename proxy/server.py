import base64
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

fd1 = open('auth.txt')
authlist = []

for line in fd1.readlines():
    t = line.strip('\n')
    temp = base64.b64encode(t.encode('utf-8')).decode('utf-8')
    authlist.append(temp)

print(authlist)

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
            details = dict(self.headers) # ignore
            print(details)

            _auth = "XXXXXXXXX"
            if 'Proxy-Authorization' in details.keys():
                _auth = details['Proxy-Authorization'].strip().split(' ')[1]
                print(_auth)

            if int(dest_ip[1]) not in range(20000,20201):
                print(">> PROXY_SERVER : Invalid request")
                threading.current_thread().join
                exit()

            if dest_ip in blacklist:
                if _auth not in authlist:
                    print(">> PROXY_SERVER : Invalid request")
                    exit()

            #Write the caching after this

            self.copyfile(urlopen(self.path), self.wfile)
            print(">> PROXY_SERVER : SUCCESS")

            # else:
            #    print(">> PROXY_SERVER : Invalid request")
            #    exit()

        except Exception as e:
            print(e)
            threading.current_thread().join
            exit()

    def do_POST(self):
        print(">> PROXY_SERVER : GET : Handling Client ",
            str(self.client_address))
        print(">> PROXY_SERVER : Thread Name:{}".format(
            threading.current_thread().name))

        dest_ip = self.path.strip("http://").split(':')
        print(dest_ip)

        print(self.requestline)  # ignore
        details = dict(self.headers)  # ignore
        print(details)

        _auth = "XXXXXXXXX"
        if 'Proxy-Authorization' in details.keys():
            _auth = details['Proxy-Authorization'].strip().split(' ')[1]
            print(_auth)

        if int(dest_ip[1]) not in range(20000, 20201):
            print(">> PROXY_SERVER : Invalid request")
            threading.current_thread().join
            exit()

        if dest_ip in blacklist:
            if _auth not in authlist:
                print(">> PROXY_SERVER : Invalid request")
                exit()

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

