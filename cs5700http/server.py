import argparse
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import signal, sys

from cs5700http import remote
from cs5700http.cache import Cache


response_cache = Cache()


def handle_term():
    def handle(sig, frame):
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle)


class GetHTTPHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # override to standard output
        sys.stdout.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format%args))
        sys.stdout.flush()

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


def main():
    parser = argparse.ArgumentParser('httpserver')

    parser.add_argument('-p', dest='port', required=True, type=int)
    parser.add_argument('-o', dest='origin', required=True)

    args = parser.parse_args()

    handle_term() # handle signal gracefully

    server = HTTPServer(('', args.port), GetHTTPHandler)
    server.origin = args.origin
    try:
        print('Starting server on port %d' % args.port)
        sys.stdout.flush()
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print('Shutting down the server')
        sys.stdout.flush()
        server.shutdown()
