import socket
from app.models.DNSResponse import DNSMessegeHeader, DNSMessegeQuestion, DNSMessegeAnswer, DNSResponseMessage, decode_dns_header, decode_dns_question, decode_dns_answer
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(buf)

            (ID, _QR, OPCODE, AA, TC, RD, RA, Z, RCODE, QDCOUNT, _ANCOUNT, NSCOUNT, ARCOUNT) = decode_dns_header(buf[:12])
            header = DNSMessegeHeader(ID, 1, OPCODE, AA, TC, RD, RA, Z, RCODE, QDCOUNT, QDCOUNT, NSCOUNT, ARCOUNT).get_header()
            print(header)
            
            names = decode_dns_question(buf, QDCOUNT)
            print(names)
            questions = b''
            answer = b''
            for (name, qtype, qclass) in names:
                question = DNSMessegeQuestion(name, qtype, qclass).get_question()
                questions += question
                answer = DNSMessegeAnswer(name, 1, 1, 60, 4, "8.8.8.8").get_answer()
                answer += answer
            print(questions)
            print(answer)
            

            response = DNSResponseMessage(header, questions, answers).get_response()
            udp_socket.sendto(response, source)

        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
