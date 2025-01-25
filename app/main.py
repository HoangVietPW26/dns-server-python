import socket
from app.models.DNSResponse import DNSMessegeHeader, DNSMessegeQuestion, DNSMessegeAnswer, DNSResponseMessage, decodeDNSHeader
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            (ID, QR, OPCODE, AA, TC, RD, RA, Z, RCODE, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT) = decodeDNSHeader(buf[:12])
            header = DNSMessegeHeader(ID, 1, OPCODE, AA, TC, RD, RA, Z, RCODE, QDCOUNT, ANCOUNT, NSCOUNT, ARCOUNT).get_header()
            question = DNSMessegeQuestion("codecrafters.io", 1, 1).get_question()
            answer = DNSMessegeAnswer("codecrafters.io", 1, 1, 60, 4, "8.8.8.8").get_answer()
            

            print(header)
            print(question)
            print(answer)
            response = DNSResponseMessage(header, question, answer).get_response()
            udp_socket.sendto(response, source)

        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
