from .Fore import Fore
from datetime import datetime

def log(content=None, content2=None, time=True):
    if time is True:
        current_time = datetime.now().strftime("%H:%M:%S")
        time_str = f"{Fore.RESET}[ {Fore.LIGHT_BLUE}{current_time}{Fore.RESET} {Fore.RESET}] "
    if content is not None:
        message = Fore.LIGHT_CYAN + content + Fore.RESET
        if "(+)" in content:
            parts = content.split("(+)")
            for i in range(1, len(parts)):
                parts[i] = f"{Fore.LIGHT_CYAN}{parts[i]}{Fore.RESET}"
            message = "(+)".join(parts).replace("(+)", f"{Fore.RESET}({Fore.GREEN}+{Fore.RESET})")
        elif "(~)" in content:
            parts2 = content.split("(~)")
            for i in range(1, len(parts2)):
                parts2[i] = f"{Fore.MAGENTA}{parts2[i]}{Fore.RESET}"
            message = "(~)".join(parts2).replace("(~)", f"{Fore.RESET}({Fore.LIGHT_BLUE}~{Fore.RESET})")
        elif "(-)" in content:
            parts3 = content.split("(-)")
            for i in range(1, len(parts3)):
                parts3[i] = f"{Fore.LIGHT_RED}{parts3[i]}{Fore.RESET}"
            message = "(-)".join(parts3).replace("(-)", f"{Fore.RESET}({Fore.RED}-{Fore.RESET})")
        message = time_str + message
        if content2 is not None:
            message = message + f"{Fore.RESET} | " + Fore.LIGHT_BLUE + content2
        print(message)