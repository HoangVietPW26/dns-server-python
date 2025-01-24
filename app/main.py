import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))
    
    while True:
        try:
            buf, source = udp_socket.recvfrom(512)

            header = b"\x04\xd2\x80\x00\x00\x01" + (b"\x00")*6
            question = b"\x0c\x63\x6F\x64\x65\x63\x72\x61\x66\x74\x65\x72\x73" + \
                b"\x02\x69\x6F" + b"\x00\x01" + b"\x00\x01" + b"\x00"
            response = header + question
    
            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
