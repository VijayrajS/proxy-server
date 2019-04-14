import base64
import socketserver, threading
from urllib.request import urlopen
from http.server import SimpleHTTPRequestHandler
import os, json, time, datetime

PORT = 20100

fd = open('blacklist.txt')
blacklist = []

cache_dir = './cache'
max_cache_buffer = no_of_occ_for_cache = 3 
logs = {}
locks = {}

if not os.path.isdir(cache_dir):
    os.makedirs(cache_dir)

# empty the cache directory
for file in os.listdir(cache_dir):
    file_name = cache_dir + '/' + file
    os.remove(file_name)

# lock fileurl
def get_access(fileurl):
    if fileurl in locks:
        lock = locks[fileurl]
    else:
        lock = threading.Lock()
        locks[fileurl] = lock
    lock.acquire()

# unlock fileurl
def leave_access(fileurl):
    if fileurl in locks:
        lock = locks[fileurl]
        lock.release()
    else:
        print("Lock problem")
        sys.exit()
 

# check if url needs to be cached
def cache_or_not(fileurl):
    try:
        log_arr = logs[fileurl]
        n = len(log_arr)
        if n < no_of_occ_for_cache:
            return False
        last_compare = log_arr[n - no_of_occ_for_cache]["datetime"]
        initial_mom = datetime.datetime.fromtimestamp(time.mktime(last_compare))
        final_mom = datetime.datetime.now()
        return final_mom - initial_mom <= datetime.timedelta(minutes=5)
            # return True
        # return False
    except Exception as e:
        print(e)
        return False

def free_cache(fileurl):
    cache_files = os.listdir(cache_dir)
    if len(cache_files) < max_cache_buffer:
        return
    for file in cache_files:
        get_access(file)
    
    last_mtime = min(logs[file][-1]['datetime'] for file in cache_files)
    file_to_del = [file for file in cache_files if logs[file][-1]["datetime"] == last_mtime][0]
    file_dir = cache_dir + '/' + file_to_del
    os.remove(file_dir)
    for file in cache_files:
        leave_access(file)

# def get_cache(client_socket, client_addr, details):
#     try:
#         client_data = details['client_data']
#         cache_path = details['cache_path']
#         do_cache = details['do_cache']
#         last_mtime = details['last_mtime']


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

class Proxy(SimpleHTTPRequestHandler):
    # Get request handler (add caching code in this function)
    def do_GET(self):
        try:
            client_addr = self.client_address
            
            if client_addr[1] not in range(20000, 20100):
                print(">> PROXY_SERVER : Invalid request")
                threading.current_thread().join
                exit()
            
            print(">> PROXY_SERVER : ", client_addr)
            print(">> PROXY_SERVER : GET : Handling Client ", str(self.client_address))
            print(">> PROXY_SERVER : Thread Name:{}".format(threading.current_thread().name))

            dest_ip = self.path.strip("http://").split(':')
            details = dict(self.headers)

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
            dest = ':'.join(dest_ip)
            #Write the caching after this
            fileurl = self.path
            print(self.path)
            if not dest in logs:
                logs[dest] = []
            dt = time.strptime(time.ctime(), "%a %b %d %H:%M:%S %Y")
            logs[dest].append({
                "datetime" : dt,
                "client" : json.dumps(client_addr),
            })
            use_cache = cache_or_not(dest)
            if use_cache:
                free_cache(dest)
                read_content = urlopen(self.path)
                content = str(read_content.read())
                content = content[1:]
                content = content.strip("\'")
                content = '\n'.join(content.split("\n"))
                print(content)
                # if fileurl.startswith('/'):
                #     fileurl = fileurl.replace('/', '', 1)
                cache_path = cache_dir + '/' + dest
                exists = os.path.isfile(cache_path)
                print(type(exists))
                if not exists:
                    print(cache_path)
                    f = open(cache_path, "w+")
                    f.write(content)
                    f.close()
                    use_cache = False
                else:
                    fd = open(cache_path, mode = "rb")
                    try:
                        self.copyfile(fd, self.wfile)
                    except Exception as e:
                        print(e)
            print(use_cache)
            if not use_cache:
                self.copyfile(urlopen(self.path), self.wfile)

            print(">> PROXY_SERVER : SUCCESS")

        except Exception as e:
            print(e)
            threading.current_thread().join
            exit()

    def do_POST(self):
        client_addr = self.client_address

        if client_addr[1] not in range(20000, 20100):
            print(">> PROXY_SERVER : Invalid request")
            threading.current_thread().join
            exit()

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
        print("PROXY_SERVER : SUCCESS")


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

