import paramiko
import threading
import sys

def listen_for_output(channel):
    while True:
        if channel.recv_ready():
            data = channel.recv(4096)
            if not data:
                break
            sys.stdout.write(data.decode(errors="ignore"))
            sys.stdout.flush()
        if channel.exit_status_ready():
            break
        
def start_interactive_session(host, username, password, port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            look_for_keys=False,
            allow_agent=False
        )
    except paramiko.AuthenticationException:
        print("[+] authentication failed")
        return
    except Exception as e:
        print(f"[!] connection error: {e}")
        return
    
    channel = client.invoke_shell()
    print(f"[+] connect to {host} - type 'exit' to quit\n")
    
    listenner = threading.Thread(target=listen_for_output, args=(channel,), daemon=True)
    listenner.start()
    
    try:
        while True:
            command = input()
            if command.strip().lower() == "exit":
                break
            channel.send(command + "\n")
    except KeyboardInterrupt:
        pass
    finally:
        channel.close()
        client.close()
        print("\n[+] session closed")