import argparse
import subprocess
import shutil
import platform
import sys
import signal
import os
import time

#Parsers
parser= argparse.ArgumentParser(description="Testing")

parser.add_argument(
    "--option",
    help="example",
    required=False
)

args = parser.parse_args()

print("Option value: ", args.option)

def print_banner():
    print('''
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣶⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣄⣀⡀⣠⣾⡇⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀
            ⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⡇⠀⠀⠀⠀
            ⠀⣶⣿⣦⣜⣿⣿⣿⡟⠻⣿⣿⣿⣿⣿⣿⣿⡿⢿⡏⣴⣺⣦⣙⣿⣷⣄⠀⠀⠀
            ⠀⣯⡇⣻⣿⣿⣿⣿⣷⣾⣿⣬⣥⣭⣽⣿⣿⣧⣼⡇⣯⣇⣹⣿⣿⣿⣿⣧⠀⠀
            ⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠸⣿⣿⣿⣿⣿⣿⣿⣷⠀
                            █████       ███   ███ 
                           ░░███       ░░░   ░░░  
  █████  █████ ████  █████  ░███████   ████  ████ 
 ███░░  ░░███ ░███  ███░░   ░███░░███ ░░███ ░░███ 
░░█████  ░███ ░███ ░░█████  ░███ ░███  ░███  ░███ 
 ░░░░███ ░███ ░███  ░░░░███ ░███ ░███  ░███  ░███ 
 ██████  ░░████████ ██████  ████ █████ █████ █████
░░░░░░    ░░░░░░░░ ░░░░░░  ░░░░ ░░░░░ ░░░░░ ░░░░░                                                                                                                                                                         
By CptWish
''')

#install cmake
def run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

def install_cmake():
    if shutil.which("cmake"):
        print("cmake already installed")
        return

    print('installing cmake')
    os_name = platform.system().lower()

    if os_name == "linux":
        if shutil.which("apt"):
            run(["sudo", "apt-get", "update"])
            run(["sudo", "apt-get", "install", "-y", "cmake"])
        elif shutil.which("dnf"):
            run(["sudo", "dnf", "install", "-y", "cmake"])
        elif shutil.which("pacman"):
            run(["sudo", "pacman", "-Sy", "--noconfirm", "cmake"])
        else:
            sys.exit("Unsupported Linux distro")

    elif os_name == "darwin":
        if not shutil.which("brew"):
            sys.exit("Homebrew not installed")
        run(["brew", "install", "cmake"])

    elif os_name == "windows":
        if shutil.which("winget"):
            run(["winget", "install", "--id", "Kitware.CMake", "-e", "--silent"])
        elif shutil.which("choco"):
            run(["choco", "install", "cmake", "-y"])
        else:
            sys.exit("No package manager found on Windows")

    else:
        sys.exit("Unsupported OS")


# #Check LLM
# def check_LLM():
#     listOutput = str(subprocess.check_output(["ls", "-l"]))

#     if not ("llama.cpp" in listOutput):
#         build_LLM()
#     else:
#         print("llama.cpp already installed ✅")


READY = False
def on_ok_signal(signum, frame):
    global READY
    READY = True

#Configure LLM
def build_LLM():
    signal.signal(signal.SIGUSR1, on_ok_signal)
    subprocess.run(["chmod", "+x", "llamaHelper.sh"])
    subprocess.Popen(["./llamaHelper.sh", str(os.getpid())], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    while not READY:
        for dots in [" ", ".", "..", "..."]:
            sys.stdout.write(f"\r[*]Configuring LLM{dots}")
            sys.stdout.flush()
            time.sleep(0.5)

    sys.stdout.write("\r[✅]Configuring LLM\n")
    sys.stdout.flush()
    print("[->]LLM is hosted on http://127.0.0.1:8080")
    #subprocess.run(["./llamaHelper.sh"])



def main():
    #print banner
    print_banner()

    #check utils
    #Check cmake
    install_cmake()

    #boot up llama
    #check_LLM()
    build_LLM()

if __name__ == "__main__":
    main()


#Reconnaissance