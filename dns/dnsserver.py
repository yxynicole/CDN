import socket
import struct

def get_sender_IP_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("www.google.com", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

class DNSPacket:

    def __init__(self, data):
        self.tid = 0
        self.flags = 0
        self.qcount = 0
        self.acount = 0
        self.nscount = 0
        self.arcount = 0
        self.qname_arr = [] # array to hold domain name elements
        self.qtype = 0
        self.qclass = 0
        self.data = data
        self.aname = 0xC00C
        self.atype = 0x0001
        self.aclass = 0x0001
        self.ttl = 100
        self.length = 4
        self.rdata = '12.45.34.1' # ip address to return in the response

    def prepare_answer(self):

        self.read_question()

        self.acount = 1
        self.arcount = 0
        self.flags = 0x8180
        answer = struct.pack('!HHHHHH', self.tid, self.flags, self.qcount, self.acount, self.nscount, self.arcount)
        answer += self.build_name_ans()
        answer += struct.pack('!HH', self.qtype, self.qclass)
        answer += struct.pack('!HHHLH4s', self.aname, self.atype, self.aclass, self.ttl, self.length, socket.inet_aton(self.rdata))
        return answer



    def read_question(self):
        [self.tid, self.flags, self.qcount, self.acount, self.nscount, self.arcount] = struct.unpack('!6H', self.data[0:12])

        self.get_q_info()


    def get_q_info(self):

        query = self.data[12:]

        begin = 0
        length = 0
        word = ''
        domain_arr = []
        end_of_domain = 0
        l = 0

        for byte in query:
            if begin == 1:
                if byte != 0:
                    word = word + chr(byte)
                l += 1
                if l == length:
                    domain_arr.append(word)
                    word = ''
                    begin = 0
                    l = 0
                if byte == 0:
                    domain_arr.append(word)
                    break
            else:
                begin = 1
                length = byte
            end_of_domain += 1


        self.qname_arr = domain_arr
        print(self.qname_arr)
        [self.qtype, self.qclass] = struct.unpack('!HH', data[12 + end_of_domain + 1: 12 + end_of_domain + 1 + 4])

    def build_name_ans(self):
        name_ans = b''

        for word in self.qname_arr:
            length = len(word)
            name_ans += bytes(length)

            for letter in word:
                name_ans += ord(letter).to_bytes(1, byteorder='big')

        return name_ans




ip = get_sender_IP_address()
print(ip)

port = 40025

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((ip, port))


while 1:

    data, addr = s.recvfrom(512)
    #dns_response = form_dns_response(data)
    dns_packet = DNSPacket(data)
    dns_answer = dns_packet.prepare_answer()
    print("yayyy")
    s.sendto(dns_answer, addr)
