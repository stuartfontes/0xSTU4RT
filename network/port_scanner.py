import socket
from concurrent.futures import ThreadPoolExecutor

def verify_port(ip, port, timeout=1):
    try:
        address_info = socket.getaddrinfo(ip, port, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        return False
    
    family, socktype, proto, _, sockaddr = address_info[0]
    sock = socket.socket(family, socktype, proto)
    sock.settimeout(timeout)
    result = sock.connect_ex(sockaddr)
    sock.close()
    
    return result == 0

def scan_ports(ip, start_port, end_port, timeout=1, max_threads=50):
    open_ports = []
    ports_to_scan = range(start_port, end_port + 1)
    
    def check_and_report(port):
        if verify_port(ip, port, timeout):
            print(f"[+] port {port} OPEN")
            return port
        return None
    
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        results = executor.map(check_and_report, ports_to_scan)
        
    open_ports = [port for port in results if port is not None]
    return open_ports