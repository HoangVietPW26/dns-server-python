import socket
import sys
from app.models.DNSResponse import (
    DNSMessegeHeader, 
    DNSMessegeQuestion, 
    DNSResponseMessage, 
    decode_dns_header, 
    decode_dns_question
)
from app.utils.utils import forward_single_query

def main(resolver=":"):
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    r_addr, r_port = resolver.split(":")
    resolver_addr = (r_addr, int(r_port))
    resolver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)
            print(buf)


            # Create response header
            (ID, _QR, OPCODE, AA, TC, RD, RA, Z, RCODE, QDCOUNT, _ANCOUNT, NSCOUNT, ARCOUNT) = decode_dns_header(buf[:12])
            response_header = DNSMessegeHeader(
                ID, 1, OPCODE, AA, TC, RD, RA, Z, 
                RCODE, QDCOUNT, QDCOUNT, NSCOUNT, ARCOUNT
            ).get_header()
            
            # Decode questions
            questions = decode_dns_question(buf, QDCOUNT)
            print(questions)

            # Prepare response components
            response_questions = b''
            response_answers = b''

            for i, (name, qtype, qclass) in enumerate(questions):
                # Create question section
                question = DNSMessegeQuestion(name, qtype, qclass).get_question()
                response_questions += question
                
                # Forward single question to resolver
                single_response = forward_single_query(resolver_socket, resolver_addr, ID, OPCODE, RD, RCODE, question)
            
                # Extract answer from resolver response
                answer_start = 12 + len(question)  # Skip header and question
                answer = single_response[answer_start:]  # Assuming fixed size A record answer
                response_answers += answer
            

            # response_header = DNSMessegeHeader(
            #     ID, 1, OPCODE, AA, TC, RD, 1, Z, RCODE,
            #     QDCOUNT, QDCOUNT,  # Same number of answers as questions
            #     0, 0
            # ).get_header()
            
            # Combine response
            response = DNSResponseMessage(
                response_header,
                response_questions,
                response_answers
            ).get_response()

            print("JJJJ")
            print(response)

            udp_socket.sendto(response, source)

        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    resolver = sys.argv[2]
    main(resolver)
