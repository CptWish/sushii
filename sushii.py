import argparse
import subprocess
import shutil
import platform
import sys

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


#Check LLM
def check_LLM():
    listOutput = str(subprocess.check_output(["ls", "-l"]))

    if not ("llama.cpp" in listOutput):
        subprocess.run(["git", "clone", "https://github.com/ggml-org/llama.cpp"])
        subprocess.run(["cd", "llama.cpp"])
        #Check if cmake is installed
        if shutil.which("cmake") is None:
            print("Cmake not installed")
    else:
        print("llama.cpp already installed ✅")

#Configure LLM
def build_LLM():
    subprocess.run(["chmod", "+x", "llamaHelper.sh"])
    subprocess.run(["./llamaHelper.sh"])



def main():
    #print banner
    print_banner()

    #check utils
    #Check cmake
    install_cmake()

    #boot up llama
    check_LLM()
    build_LLM()

if __name__ == "__main__":
    main()


#Reconnaissance