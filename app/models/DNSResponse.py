class DNSMessegeHeader():
    def __init__(self, ID=0, QR=0, OPCODE=0, AA=0, TC=0, RD=0, RA=0, Z=0, RCODE=0, QDCOUNT=1, ANCOUNT=0, NSCOUNT=0, ARCOUNT=0):
        self.id = ID.to_bytes(2, 'big')
        # Pack flags into two bytes
        self.flags = self.get_flags(QR, OPCODE, AA, TC, RD, RA, Z, RCODE)
        self.qdcount = QDCOUNT.to_bytes(2, 'big')
        self.ancount = ANCOUNT.to_bytes(2, 'big')
        self.nscount = NSCOUNT.to_bytes(2, 'big')
        self.arcount = ARCOUNT.to_bytes(2, 'big')
    
    def get_flags(self, QR, OPCODE, AA, TC, RD, RA, Z, RCODE):
        flags = (QR << 15) | (OPCODE << 11) | (AA << 10) | (TC << 9) | \
                (RD << 8) | (RA << 7) | (Z << 4) | RCODE
        return flags.to_bytes(2, 'big')
    def get_header(self):
        return self.id + self.flags + self.qdcount + self.ancount + self.nscount + self.arcount

def decode_dns_header(header):
    ID = int.from_bytes(header[:2], 'big')
    flags = int.from_bytes(header[2:4], 'big')
    QR = (flags & 0b1000000000000000) >> 15
    OPCODE = (flags & 0b0111100000000000) >> 11
    AA = (flags & 0b0000010000000000) >> 10
    TC = (flags & 0b0000001000000000) >> 9
    RD = (flags & 0b0000000100000000) >> 8
    RA = (flags & 0b0000000010000000) >> 7
    Z = (flags & 0b0000000001111000) >> 4
    # RCODE = flags & 0b0000000000001111
    RCODE = 0 if OPCODE == 0 else 4
    QDCOUNT = int.from_bytes(header[4:6], 'big')
    ANCOUNT = int.from_bytes(header[6:8], 'big')
    NSCOUNT = int.from_bytes(header[8:10], 'big')
    ARCOUNT = int.from_bytes(header[10:12], 'big')
    return ID, QR, OPCODE, AA, TC, RD, RA, Z, RCODE, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT

class DNSMessegeQuestion():
    def __init__(self, NAME="codecrafters.io", QTYPE=1, QCLASS=1):
        self.name = self.get_name(NAME)
        self.qtype = QTYPE.to_bytes(2, 'big')
        self.qclass = QCLASS.to_bytes(2, 'big')
    
    def get_name(self, NAME):
        names = NAME.split('.')
        for i in range(len(names)):
            names[i] = len(names[i]).to_bytes(1, 'big') + names[i].encode("utf-8")
        self.name = b''.join(names) + b'\x00'
        return self.name

    
    def get_question(self):
        return self.name + self.qtype + self.qclass

def decode_dns_question(question, num_of_question=1, start=12):
    names = []
    name = []
    i = start

    while num_of_question > 0:
        while question[i] != 0:
            print(question[i], i)
            if question[i] >= 192:
                offset = int.from_bytes(question[i:i+2], 'big') - 49152
                name.append(decode_compress(question, offset))
                i += 1
                break
            length = question[i]
            name.append(question[i+1:i+1+length].decode("utf-8"))
            i += length + 1
        qtype = int.from_bytes(question[i+1:i+3], 'big')
        qclass = int.from_bytes(question[i+3:i+5], 'big')
        names.append(('.'.join(name), qtype, qclass))
        name = []
        i += 5
        num_of_question -= 1

    return names

def decode_compress(question, offset):
    name = []
    i = offset
    while question[i] != 0:
        length = question[i]
        name.append(question[i+1:i+1+length].decode("utf-8"))
        i += length + 1
    return '.'.join(name)

    
class DNSMessegeAnswer():
    def __init__(self, NAME="codecrafters.io", TYPE=1, CLASS=1, TTL=60, RDLENGTH=4, RDATA="8.8.8.8"):
        self.name = self.get_name(NAME)
        self.type = TYPE.to_bytes(2, 'big')
        self.class_ = CLASS.to_bytes(2, 'big')
        self.ttl = TTL.to_bytes(4, 'big')
        self.rdlength = RDLENGTH.to_bytes(2, 'big')
        self.rdata = self.get_ip(RDATA)
    
    def get_name(self, NAME):
        names = NAME.split('.')
        for i in range(len(names)):
            names[i] = len(names[i]).to_bytes(1, 'big') + names[i].encode("utf-8")
        self.name = b''.join(names) + b'\x00'
        return self.name
    
    def get_ip(self, IP):
        ip_bytes = bytes(map(int, IP.split('.')))
        print(ip_bytes)  # b'\xc0\xa8\x01\x01'
        return ip_bytes
    
    def get_answer(self):
        return self.name + self.type + self.class_ + self.ttl + self.rdlength + self.rdata

def decode_dns_answer(answer, start=0):
    name = []
    i = start
    while answer[i] != 0:
        length = answer[i]
        name.append(answer[i+1:i+1+length].decode("utf-8"))
        i += length + 1
    qtype = int.from_bytes(answer[i+1:i+3], 'big')
    qclass = int.from_bytes(answer[i+3:i+5], 'big')
    ttl = int.from_bytes(answer[i+5:i+9], 'big')
    rdlength = int.from_bytes(answer[i+9:i+11], 'big')
    rdata = '.'.join(map(str, answer[i+11:i+11+rdlength]))
    return '.'.join(name)
class DNSResponseMessage():
    def __init__(self, header, question, answer):
        self.header = header
        self.question = question
        self.answer = answer
    
    def get_response(self):
        return self.header + self.question + self.answer
