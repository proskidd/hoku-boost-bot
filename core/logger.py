from colorama import Fore
import time

class logger:
    def __init__(self):
        self.times = time.strftime("%H:%M:%S")

    def success(self, msg: str):
        print(f"{Fore.WHITE}[{Fore.LIGHTBLUE_EX}{self.times}{Fore.RESET}] ({Fore.GREEN}+{Fore.RESET}) {Fore.GREEN}{msg}{Fore.RESET}")

    def info(self, msg: str):
        print(f"[{Fore.LIGHTBLUE_EX}{self.times}{Fore.RESET}] ({Fore.YELLOW}!{Fore.RESET}) {Fore.YELLOW}{msg}{Fore.RESET}")

    def error(self, msg: str):
        print(f"[{Fore.LIGHTBLUE_EX}{self.times}{Fore.RESET}] ({Fore.RED}-{Fore.RESET}) {Fore.RED}{msg}{Fore.RESET}")