import argparse 
from network.port_scanner import scan_ports
from network.traceroute import trace_route, parse_trace_route
from network.banner_grabber import grab_banner
from network.os_detector import get_ttl, guess_os
from network.arp_scanner import arp_scan

def main():
    parser = argparse.ArgumentParser(description="0xSTU4RT - multifunctional forensic tool")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    network_parser = subparsers.add_parser("network", help="network analysis tools")
    network_parser.add_argument("--scan-ports", metavar="IP", help="IP or hostname for scan ports")
    network_parser.add_argument("--start", type=int, default=1, help="initial port (default: 1)")
    network_parser.add_argument("--end", type=int, default=1024, help="final port (default: 1024)")
    network_parser.add_argument("--trace", metavar="TARGET", help="trace route to a host")
    network_parser.add_argument("--banner", metavar="TARGET", help="grab service banner from a target")
    network_parser.add_argument("--port", type=int, help="port to use with --banner")
    network_parser.add_argument("--detect-os", metavar="TARGET", help="guess the OS of a target via TTL")
    network_parser.add_argument("--arp-scan", metavar="RANGE", help="scan local network by arp (e.g. 192.x.x.0/24")
    
    args = parser.parse_args()
    
    if args.command == "network":
        if args.scan_ports:
            print(f"[+] scanning {args.scan_ports} (ports {args.start} - {args.end})...")
            open_ports = scan_ports(args.scan_ports, args.start, args.end)
            print(f"[-] total: {len(open_ports)} open ports of {args.end - args.start + 1} scanned")
        
        if args.trace:
            print(f"[+] tracing route to {args.trace}...")
            raw = trace_route(args.trace)
            hops = parse_trace_route(raw)
            for hop in hops:
                ip_display = hop["ip"] if hop["ip"] else "* (timeout)"
                print(f" HOP {hop['hop']}: {ip_display}")
        
        if args.banner:
            if not args.port:
                print("[!] error: -banner requires --port")
            else:
                print(f"[+] grabbing banner from {args.banner}:{args.port}...")
                banner = grab_banner(args.banner, args.port)
                if banner:
                    print(f"[+] banner: {banner}")
                else:
                    print("[-] no banner received")
                    
        if args.detect_os:
            print(f"[+] detecting OS of {args.detect_os}...\n[+] linux -> 64~\n[+] windows -> 128~\n[+] network device -> 255~")
            ttl = get_ttl(args.detect_os)
            result = guess_os(ttl)
            print(f"[+] TTL: {ttl} -> {result}")
            
        if args.arp_scan:
            print(f"[+] scanning local network {args.arp_scan}...")
            devices = arp_scan(args.arp_scan)
            print(f"[-] {len(devices)} device(s) found:")
            for device in devices:
                print(f"FOUND: {device['ip']} -> {device['mac']}")
                    
            
if __name__ == "__main__":
    main()
    
    