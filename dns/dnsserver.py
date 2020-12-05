import socket
import struct
import argparse

def get_sender_IP_address():
    '''
    Returns the ip address of the local machine
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("www.google.com", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

class DNSPacket:
    '''
    A class to represent a DNS packet
    Will be used to parse incoming dig request and form a DNS A record response
    '''

    def __init__(self):

        #Header fields
        self.tid = 0
        self.flags = 0
        self.qcount = 0
        self.acount = 0
        self.nscount = 0
        self.arcount = 0

        #Query fields
        self.qname_arr = [] #array to represent the elements (delimited by .) of the qname
        self.qtype = 0
        self.qclass = 0

        #Answer fields to be used in response
        self.name_ans = 0
        self.type_ans = 0
        self.class_ans = 0
        self.ttl_ans = 0
        self.length_ans = 0
        self.data_ans = ''

    def intake_question(self, data):
        '''
        Reads an inital DNS question from requester and parses the questions
        Sets the values for id, flags, qcount, acount, nscount, arcount, qname,
        qtype, and qclass
        '''

        #Unpack header
        [self.tid, self.flags, self.qcount, self.acount, self.nscount, self.arcount] = struct.unpack('!6H', data[0:12])

        #In python 2, the socket.recvfrom method returns a string, in python3
        # it returns bytes.  Tweak the below code so it works with python 3
        # need to convert data from bytes to string

        domain = data[12:-4] # the domain being requested
        i = 0
        domain_words = []
        while True:
            j = ord(domain[i])
            if j == 0:
                break
            i += 1
            domain_words.append(domain[i:i+j])
            i += j
        self.qname_arr = domain_words #domain words delimited by period

        [self.qtype, self.qclass] = struct.unpack('!HH', data[12+i+1:12+i+1+4])

    def form_answer(self, ip_addr):
        '''
        Forms a DNS "A" record response that can be returned to caller
        '''

        self.arcount = 0
        self.acount = 1
        self.flags = 0x8180

        #DNS Header
        answer = struct.pack('!HHHHHH', self.tid, self.flags, self.qcount,
                             self.acount, self.nscount, self.arcount)

        #Name
        answer += ''.join(chr(len(w)) + w for w in self.qname_arr)
        answer += '\x00'

        #Type and class
        answer += struct.pack('!HH', self.qtype, self.qclass)

        #Remainder of answer
        self.name_ans = 0xC00C
        self.type_ans = 0x0001
        self.class_ans = 0x0001
        self.ttl_ans = 60
        self.length_ans = 4
        self.data_ans = ip_addr #IP address to be returned for the domain requested
                                # TODO: Need to update this. Hardcoded ip for now

        answer += struct.pack('!HHHLH4s', self.name_ans, self.type_ans, self.class_ans,
                          self.ttl_ans, self.length_ans, socket.inet_aton(self.data_ans))
        return answer

def start_dns_server(ip, port):
    '''
    Creates a socket and listens for data
    Assumes all data will be incoming DNS questions
    For each DNS packet receives, forms a response and replies with an A record
    UPDATE THIS Replies with a hardcoded IP address for now UPDATE THIS
    '''

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))


    #DO WE NEED TO ADD THREADING?

    while True:
        data, addr = s.recvfrom(512)
        print("received data")
        dns_packet = DNSPacket()
        dns_packet.intake_question(data)
        dns_answer = dns_packet.form_answer('34.238.192.84') #hardcoded virgina ec2 server
        print("about to send dns response")
        s.sendto(dns_answer, addr)

def main(args):
    ip = get_sender_IP_address()
    start_dns_server(ip, args.port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', type=int, required=True)
    parser.add_argument('--name', '-n', required=True) # Not sure why we need this? Not using it as of yet
    args = parser.parse_args()
    main(args)
