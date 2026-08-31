import socket

def verificar_porta(ip, porta, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    resultado = sock.connect_ex((ip, porta))
    sock.close()
    return resultado == 0                                                                                                                                                     