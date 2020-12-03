import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests


class GetHTTPHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.log_request()

        try:
            resp = requests.get('http://' + self.server.origin + self.path)
        except Exception as e:
            self.log_error('Error: %s', e)
            status_code = 500
            content = ''
        else:
            status_code = resp.status_code
            content = resp.content

        if hasattr(content, 'encode'):
            content = content.encode()

        self.send_response(status_code)
        self.end_headers()
        self.wfile.write(content)


def main(args):
    print('Starting server on port %d' % args.port)

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