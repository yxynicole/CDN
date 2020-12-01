import socketserver
import argparse

parser = argparse.ArgumentParser('dnsserver')

parser.add_argument('-p', dest='port', required=True, type=int)
parser.add_argument('-n', dest='name', required=True)

domain_to_resolve = None

class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        print('Raw UDP DNS request -', data)
        socket.sendto(data, self.client_address)


if __name__ == "__main__":
    args = parser.parse_args()

    domain_to_resolve = args.name

    server = socketserver.UDPServer(('localhost', args.port), UDPHandler)

    try:
        print('Starting server on port %d' % args.port)
        server.serve_forever()
    except KeyboardInterrupt:
        print('Teminated from keyboard')
    finally:
        server.shutdown()
