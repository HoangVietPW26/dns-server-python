from app.models.DNSResponse import DNSMessegeHeader

def forward_single_query(resolver_socket, resolver_addr, query_id, op_code, rd, rcode, question):
    # Create a new DNS query with single question
    header = DNSMessegeHeader(
        query_id, 0, op_code, 0, 0, rd, 0, 0, rcode, 
        1,  # QDCOUNT = 1
        0, 0, 0
    ).get_header()
    
    query = header + question
    
    # Send to resolver and get response
    resolver_socket.sendto(query, resolver_addr)
    response, _ = resolver_socket.recvfrom(512)
    return response