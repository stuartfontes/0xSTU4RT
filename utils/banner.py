import pyfiglet
from colorama import init, Fore, Style

init(autoreset=True)

def show_banner():
    ascii_art = pyfiglet.figlet_format("0xSTU4RT", font="larry3d")

    print(Fore.GREEN + ascii_art)
    print(Fore.GREEN + "    [+] Multifunctional Forensic Tool")
    print(Fore.GREEN + "    [+] GitHub:   " + "https://github.com/stuartfontes")
    print(Fore.GREEN + "    [+] LinkedIn: " + "https://www.linkedin.com/in/mauricio-stuart-fontes-83b45318a/")
    print(Style.RESET_ALL)