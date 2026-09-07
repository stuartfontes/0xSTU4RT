from network.ssh_interactive import start_interactive_session
import getpass

host = input("Host: ")
username = input("Username: ")
password = getpass.getpass("Password: ")

start_interactive_session(host, username, password)