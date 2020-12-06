import argparse
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

import remote
from cache import Cache
import utils

response_cache = Cache()

def get_sender_IP_address():
    '''
    Returns the ip address of the local machine
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("www.google.com", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

class GetHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_request()

        if response_cache.has(self.path):
            self.log_message('using cache for path: %s', self.path)
            content = response_cache.get(self.path)
            status_code = 200
            error = None
        else:
            self.log_message('requesting from origin for path: %s', self.path)
            status_code, content, error = remote.get(self.server.origin, self.path)
            if error is None:
                value = status_code, content, error
                # response_cache.set(self.path, value)

        if error:
            self.log_error('Error: %s', error)

        if hasattr(content, 'encode'):
            content = content.encode()

        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(content)


def main(args):
    print('Starting server on port %d in thread %d' % (args.port, os.getpid()))
    print(get_sender_IP_address())

    server = HTTPServer(('', args.port), GetHTTPHandler)
    server.origin = args.origin
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Teminated from keyboard')
    finally:
        server.shutdown()

if __name__ == '__main__':
    parser = argparse.ArgumentParser('httpserver')

    parser.add_argument('-p', dest='port', required=True, type=int)
    parser.add_argument('-o', dest='origin', required=True)

    utils.handle_term() # handle signal gracefully

    main(parser.parse_args())