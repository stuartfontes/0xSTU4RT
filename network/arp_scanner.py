from scapy.all import ARP, Ether, srp

def arp_scan(ip_range, timeout=2):
    arp_request = ARP(pdst=ip_range)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = broadcast / arp_request
    
    answered, unanswered = srp(packet, timeout=timeout, verbose=False)
    
    devices = []
    for sent, received in answered:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})
        
    return devices