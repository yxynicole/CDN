import argparse
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

import remote
from cache import Cache

response_cache = Cache()

class GetHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_request()

        if response_cache.has(self.path):
            self.log_message('using cache for path: %s', self.path)
            status_code, content, error = response_cache.get(self.path)
        else:
            self.log_message('requesting from origin for path: %s', self.path)
            status_code, content, error = remote.get(self.server.origin, self.path)
            if error is None:
                value = status_code, content, error
                response_cache.set(self.path, value)

        if error:
            self.log_error('Error: %s', error)

        if hasattr(content, 'encode'):
            content = content.encode()

        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(content)


def main(args):
    print('Starting server on port %d in thread %d' % (args.port, os.getpid()))

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

    main(parser.parse_args())