#!/usr/bin/env python

from http.server import ThreadingHTTPServer, HTTPServer

# HTTPRequestHandler class

class testHTTPServer_RequestHandler(ThreadingHTTPServer):

    # GET
    def do_GET(self):
        # Send response status code
        pass

def run():
    print('starting server...')
    server_address = ('127.0.0.1', 20100)
    httpd = ThreadingHTTPServer(server_address, testHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()

run()
