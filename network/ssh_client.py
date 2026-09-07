import paramiko

def run_ssh_command(host, username, password, command, port=22, timeout=10):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    
    try:
        client.connect(
            hostname=host, 
            port=port, 
            username=username, 
            password=password, 
            timeout=timeout,
            look_for_keys=False,
            allow_agent=False
            )
        
        stdin, stdout, stderr = client.exec_command(command)
        
        output = stdout.read().decode(errors="ignore")
        error = stderr.read().decode(errors="ignore")
        
        return {"output": output, "error": error}
    except paramiko.AuthenticationException:
        return {"output":"", "error": "authentication failed"}
    except Exception as e:
        return {"output": "", "error": str(e)}
    finally:
        client.close()