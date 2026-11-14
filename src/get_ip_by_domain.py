import socket

async def get_ip_by_domain(domain):
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        return None

