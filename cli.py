import argparse
import json
import getpass
from utils.banner import show_banner
from network.port_scanner import scan_ports
from network.traceroute import trace_route, parse_trace_route
from network.banner_grabber import grab_banner
from network.os_detector import get_ttl, guess_os
from network.arp_scanner import arp_scan
from network.dns_checker import check_dns
from network.ssh_client import run_ssh_command
from network.ssh_interactive import start_interactive_session
from network.geolocator import geolocate

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="0xSTU4RT - multifunctional forensic tool")
    subparsers = parser.add_subparsers(dest="command", required=True)

    network_parser = subparsers.add_parser("network", help="network analysis tools")
    network_parser.add_argument("--scan-ports", metavar="IP", help="IP or hostname for scan ports")
    network_parser.add_argument("--start", type=int, default=1, help="initial port (default: 1)")
    network_parser.add_argument("--end", type=int, default=1024, help="final port (default: 1024)")
    network_parser.add_argument("--trace", metavar="TARGET", help="trace route to a host")
    network_parser.add_argument("--banner", metavar="TARGET", help="grab service banner from a target")
    network_parser.add_argument("--port", type=int, default=22, help="port to use with --banner or --ssh (default: 22)")
    network_parser.add_argument("--detect-os", metavar="TARGET", help="guess the OS of a target via TTL")
    network_parser.add_argument("--arp-scan", metavar="RANGE", help="scan local network via ARP (e.g. 192.168.1.0/24)")
    network_parser.add_argument("--dns", metavar="DOMAIN", help="check DNS records of a domain")
    network_parser.add_argument("--ssh", metavar="HOST", help="connect to a host via SSH")
    network_parser.add_argument("--user", metavar="USERNAME", help="username to use with --ssh")
    network_parser.add_argument("--run", metavar="COMMAND", help="run a single command via --ssh instead of an interactive session")
    network_parser.add_argument("--geo", metavar="IP", help="geolocate a public IP address (offline, MaxMind GeoLite2)")
    
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
                print(f"  Hop {hop['hop']}: {ip_display}")

        if args.banner:
            print(f"[+] grabbing banner from {args.banner}:{args.port}...")
            banner = grab_banner(args.banner, args.port)
            if banner:
                print(f"[+] banner: {banner}")
            else:
                print("[-] no banner received")

        if args.detect_os:
            print(f"[+] detecting OS of {args.detect_os}...")
            ttl = get_ttl(args.detect_os)
            result = guess_os(ttl)
            print(f"[+] TTL: {ttl} -> {result}")

        if args.arp_scan:
            print(f"[+] scanning local network {args.arp_scan}...")
            devices = arp_scan(args.arp_scan)
            print(f"[-] {len(devices)} device(s) found:")
            for device in devices:
                print(f"    {device['ip']}  ->  {device['mac']}")

        if args.dns:
            print(f"[+] checking DNS records for {args.dns}...")
            records = check_dns(args.dns)
            print(json.dumps(records, indent=2))

        if args.ssh:
            if not args.user:
                print("[!] error: --ssh requires --user")
            else:
                password = getpass.getpass(f"Password for {args.user}@{args.ssh}: ")

                if args.run:
                    result = run_ssh_command(args.ssh, args.user, password, args.run, port=args.port)
                    if result["output"]:
                        print(result["output"])
                    if result["error"]:
                        print(f"[!] {result['error']}")
                else:
                    start_interactive_session(args.ssh, args.user, password, port=args.port)
                    
        if args.geo:
            print(f"[+] geolocating {args.geo}...")
            result = geolocate(args.geo)
            if "error" in result:
                print (f"[!] {result['error']}")
            else:
                print(f"[+] country: {result['country']}\n"
                      f"[+] city: {result['city']}\n"
                      f"[+] coordinates: {result['latitude'], {result['longitude']}}\n")

if __name__ == "__main__":
    main()