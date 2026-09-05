import socket 

def grab_banner(ip, port , timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        
        banner = sock.recv(1024)
        sock.close()
        
        return banner.decode(errors="ignore").strip()
    except (socket.timeout, ConnectionRefusedError, OSError):
        return None