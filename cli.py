import argparse 
from network.port_scanner import scan_ports

def main():
    parser = argparse.ArgumentParser(description="0xSTU4RT - multifunctional forensic tool")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    network_parser = subparsers.add_parser("network", help="network analysis tools")
    network_parser.add_argument("--scan-ports", metavar="IP", help="IP or hostname for scan ports")
    network_parser.add_argument("--start", type=int, default=1, help="initial port (default: 1)")
    network_parser.add_argument("--end", type=int, default=1024, help="final port (default: 1024)")
    
    args = parser.parse_args()
    
    if args.command == "network":
        if args.scan_ports:
            print(f"[+] scanning {args.scan_ports} (ports {args.start} - {args.end})...")
            open_ports = scan_ports(args.scan_ports, args.start, args.end)
            print(f"[-] total: {len(open_ports)} open ports of {args.end - args.start + 1} scanned")
            
if __name__ == "__main__":
    main()
    
    