import http.server
import socketserver

PORT = 20111

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Handler) as httpd:
    try:
        print("serving at port", PORT)
        httpd.serve_forever()

    except KeyboardInterrupt:
        httpd.shutdown()

    except Exception as _exc:
        print(_exc)
        httpd.shutdown()
