#new comment

from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 40025

class helloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write("helloooo".encode())

def main():
    server = HTTPServer(('', PORT), helloHandler)
    print('Server running on port %s' % PORT )
    server.serve_forever()

if __name__ == '__main__':
    main()
