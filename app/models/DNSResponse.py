class DNSMessegeHeader():
    def __init__(self, ID=0, QR=0, OPCODE=0, AA=0, TC=0, RD=0, RA=0, Z=0, RCODE=0, QDCOUNT=1, ANCOUNT=0, NSCOUNT=0, ARCOUNT=0):
        self.id = ID.to_bytes(2, 'big')
        self.qr = QR.to_bytes(1, 'big')
        self.opcode = OPCODE.to_bytes(1, 'big')
        self.aa = AA.to_bytes(1, 'big')
        self.tc = TC.to_bytes(1, 'big')
        self.rd = RD.to_bytes(1, 'big')
        self.ra = RA.to_bytes(1, 'big')
        self.z = Z.to_bytes(1, 'big')
        self.rcode = RCODE.to_bytes(1, 'big')
        self.qdcount = QDCOUNT.to_bytes(2, 'big')
        self.ancount = ANCOUNT.to_bytes(2, 'big')
        self.nscount = NSCOUNT.to_bytes(2, 'big')
        self.arcount = ARCOUNT.to_bytes(2, 'big')
    
    def get_header(self):
        return self.id + self.qr + self.opcode + self.aa + self.tc + self.rd + self.ra + self.z + self.rcode + self.qdcount + self.ancount + self.nscount + self.arcount

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

class DNSResponseMessage():
    def __init__(self, header, question, answer):
        self.header = header
        self.question = question
        self.answer = answer
    
    def get_response(self):
        return self.header + self.question + self.answer
