import colorama
import sys
import const

def progress_bar(completed, total, content, length=20):
    progress = int(completed / total * length)
    bar = f"[{colorama.Fore.GREEN}{'█' * progress}{colorama.Fore.WHITE}{'█' * (length - progress)}{colorama.Fore.RESET}] - {content}"
    
    print(f"\r {bar}")
    sys.stdout.flush()