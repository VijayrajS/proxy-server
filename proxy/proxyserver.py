from socket import *
import _thread

# This funciton initializes socket and starts listening.
# When connection request is made, a new thread is created to serve the request
def start_proxy_server():

    # Initialize socket
    try:
        proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_socket.bind(('', proxy_port))
        proxy_socket.listen(max_connections)

        print("[] Serving proxy on " + str(proxy_socket.getsockname()[0]) + "port " + str(proxy_socket.getsockname()[1])


    except:
        print("* ERROR STARTING PROXY SERVER")
        proxy_socket.close()
        exit()
    
    # Main loop
    while True:
        try:
            client_socket, client_addr = proxy_socket.accept()
            client_data = client_socket.recv(BUFFER_SIZE)

            print "%s - - [%s] \"%s\"" % (
                str(client_addr),
                str(datetime.datetime.now()),
                client_data.splitlines()[0]
            )

            _thread.start_new_thread(
                handle_one_request_,
                (
                    client_socket,
                    client_addr,
                    client_data
                )
            )

        except KeyboardInterrupt:
            client_socket.close()
            proxy_socket.close()
            print("[] User request to end proxy server")
            break
