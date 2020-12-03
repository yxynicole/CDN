#new comment

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request
import socket

PORT = 40025

def get_sender_IP_address():
    '''
    Returns the ip address of the local machine
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("www.google.com", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

        # this is the origin site.  we need to accept "Main_Page" (or whatever pager the user is requesting)
        # as a paremeter in the get request
        request_url = urllib.request.urlopen('http://ec2-18-207-254-152.compute-1.amazonaws.com:8080/wiki/Main_Page')

        # sends the html back to the GET requester
        self.wfile.write(request_url.read())

def main():

    print(get_sender_IP_address())
    server = HTTPServer(('', PORT), Handler)
    print('Server running on port %s' % PORT )
    server.serve_forever()

if __name__ == '__main__':
    main()
