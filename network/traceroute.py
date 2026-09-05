import re
import subprocess
import platform

def trace_route(target):
    system = platform.system()

    if system == "Windows":
        command = ["tracert", "-d", target]
    else:
        command = ["traceroute", "-n", target]

    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    return result.stdout

def parse_trace_route(raw_output):
    hops = []
    ipv4_pattern = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    ipv6_pattern = r"^[0-9a-fA-F:]+$"

    for line in raw_output.splitlines():
        line = line.strip()
        if not line or not line[0].isdigit():
            continue

        parts = line.split()
        hop_number = parts[0]
        found_ip = None

        for part in parts[1:]:
            if re.match(ipv4_pattern, part):
                found_ip = part
                break
            if re.match(ipv6_pattern, part) and ":" in part:
                found_ip = part
                break

        hops.append({"hop": hop_number, "ip": found_ip})

    return hops