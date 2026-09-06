import subprocess
import platform
import re

def get_ttl(target):
    system = platform.system()
    
    if system == "Windows":
        command = ["ping", "-n", "1", target]
    else:
        command = ["ping", "-c", "1", target]
        
    result = subprocess.run(command, capture_output=True, text=True, timeout=10)
    output = result.stdout
    
    match = re.search(r"[Tt][Tt][Ll]=(\d+)", output)
    if match:
        return int(match.group(1))
    return None

def guess_os(ttl):
    if ttl is None:
        return "unknown (no answer)"
    if ttl <= 64:
        return "probably Linux/Unix"
    elif ttl <= 128:
        return "problably Windows"
    else:
        return "problably network device (switch/router)"