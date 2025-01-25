import socket
from app.models.DNSResponse import DNSMessegeHeader, DNSMessegeQuestion, DNSMessegeAnswer, DNSResponseMessage
def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)

            # header = (b"\x04\xd2" +  # ID: 1234
            #           b"\x80" +      # QR=1, OPCODE=0, etc.
            #           b"\x00" +      # More flags
            #           b"\x00\x01" +  # QDCOUNT: 1 question
            #           b"\x00\x01" +  # ANCOUNT: 1 answer
            #           b"\x00\x00" +  # NSCOUNT: 0
            #           b"\x00\x00")   # ARCOUNT: 0
            
            header = DNSMessegeHeader(1234, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0).get_header()

            # Question Section
            # question = (b"\x0ccodecrafters\x02io\x00" +   # Name 
            #         b"\x00\x01" +  # Type: A record 
            #         b"\x00\x01")    # Class: IN

            question = DNSMessegeQuestion("codecrafters.io", 1, 1).get_question()


            # Answer Section
            # answer = (b"\x0ccodecrafters\x02io\x00" +  # Name
            #         b"\x00\x01" +  # Type: A record
            #         b"\x00\x01" +  # Class: IN
            #         b"\x00\x00\x00\x3c" +  # TTL: 60
            #         b"\x00\x04" +  # Length: 4 bytes
            #         b"\x08\x08\x08\x08")  # IP: 8.8.8.8

            answer = DNSMessegeAnswer("codecrafters.io", 1, 1, 60, 4, "8.8.8.8").get_answer()
            

            response = DNSResponseMessage(header, question, answer).get_response()
    
            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
