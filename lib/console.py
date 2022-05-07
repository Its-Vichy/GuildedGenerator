from colorama import Fore, init; init()
import threading, json, os

__config__ = json.load(open('./script/config.json', 'r+'))
lock = threading.Lock()

class Console:
    @staticmethod
    def debug(content: str) -> None:
        if __config__['debug']:
            lock.acquire()
            print(f'[DEBUG] {content}{Fore.RESET}'.replace('[+]', f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}]').replace('[*]', f'[{Fore.LIGHTYELLOW_EX}*{Fore.RESET}]').replace('[>]', f'[{Fore.CYAN}>{Fore.RESET}]').replace('[-]', f'[{Fore.RED}-{Fore.RESET}]'))
            lock.release()

    @staticmethod
    def printf(content: str) -> None:
        lock.acquire()
        print(content.replace('[+]', f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}]').replace('[*]', f'[{Fore.LIGHTYELLOW_EX}*{Fore.RESET}]').replace('[>]', f'[{Fore.CYAN}>{Fore.RESET}]').replace('[-]', f'[{Fore.RED}-{Fore.RESET}]'))
        lock.release()
    
    @staticmethod
    def print_logo() -> None:
        os.system('cls && title GuildeadGen - github.com/its-vichy' if os.name == 'nt' else 'clear')
        print(Fore.LIGHTWHITE_EX + '''
          _____     _ __   __            __
         / ___/_ __(_) /__/ /__ ___ ____/ /
        / (_ / // / / / _  / -_) _ `/ _  / 
        \___/\_,_/_/_/\_,_/\__/\_,_/\_,_/...                           
        ''')