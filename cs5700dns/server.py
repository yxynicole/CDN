import socketserver
import argparse
import struct
from socket import inet_aton
import signal, sys

from cs5700dns import resolver


def handle_term():
    def handle(sig, frame):
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle)


class Buffer:
    def __init__(self, data):
        self.i = 0
        self.data = data

    def move(self, n):
        self.i += n
    
    def peek(self, length):
        return self.data[self.i:self.i+length]

    def read(self, length=None):
        if length is None:
            length = len(self.data) - self.i
        data = self.peek(length)
        self.move(length)
        return data

class DNSPacket:
    def __init__(self, data):
        self.buf = Buffer(data)
        self.data_ans = None

    def unpack(self):
        self.tid, self.flags, self.qcount = struct.unpack('!3H', self.buf.read(6))
        self.acount, self.nscount, self.arcount = struct.unpack('!3H', self.buf.read(6))

        self.qname_arr = []
        while True:
            length = ord(self.buf.read(1))
            if length == 0:
                break
            word = self.buf.read(length)
            if hasattr(word, 'decode'):
                word = word.decode()
            self.qname_arr.append(word)

        self.qtype, self.qclass = struct.unpack('!2H', self.buf.read(4))
        self.additional_data = self.buf.read()

    def answer(self, ip_addr):
        self.acount = 1
        self.arcount = 0
        self.flags = 0x8180
        self.name_ans = 0xC00C
        self.type_ans = 0x0001
        self.class_ans = 0x0001
        self.ttl_ans = 60
        self.length_ans = 4
        self.data_ans = ip_addr

    def reject(self):
        self.nscount = 1
        self.flags = 0x8183
        self.data_ans = None

    def pack(self):
        answer = struct.pack('!HHHHHH', self.tid, self.flags, self.qcount,
                             self.acount, self.nscount, self.arcount)
        for name in self.qname_arr:
            if hasattr(name, 'encode'):
                name = name.encode()
            answer += struct.pack('!B', len(name)) + name
        answer += struct.pack('!B', 0)

        #Type and class
        answer += struct.pack('!HH', self.qtype, self.qclass)
        if self.data_ans is not None:
            answer += struct.pack('!HHHLH4s', self.name_ans, self.type_ans, self.class_ans,
                              self.ttl_ans, self.length_ans, self.data_ans)
        return answer

class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data, socket = self.request
        buf = Buffer(data)
        # print('Raw UDP DNS request -', data)

        dns_packet = DNSPacket(data)
        dns_packet.unpack()

        domain_received = '.'.join(dns_packet.qname_arr)

        replica_addr = resolver.resolve(domain_received, self.client_address)
        if replica_addr:
            print('domain matches -', domain_received, '- replica address -', replica_addr)
            sys.stdout.flush()
            dns_packet.answer(inet_aton(replica_addr))
        else:
            print('unmatched domain -', domain_received)
            sys.stdout.flush()
            dns_packet.reject()

        socket.sendto(dns_packet.pack(), self.client_address)


def main():
    parser = argparse.ArgumentParser('dnsserver')

    parser.add_argument('-p', dest='port', required=True, type=int)
    parser.add_argument('-n', dest='name', required=True)

    args = parser.parse_args()

    resolver.set_domain(args.name)

    server = socketserver.UDPServer(('0.0.0.0', args.port), UDPHandler)
    handle_term()
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

if __name__ == "__main__":
    main()
