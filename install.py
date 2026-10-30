import os
import subprocess
import sys

version = "v0.1"
dependencies = ["tree", "git", "curl"]
gitProjectLink = "https://github.com/Asterlenist/sysadmintools"

print("Installer ", version)

while True:
    packageManager = input("Write your Package Manager (example: apt) ")
    result = subprocess.run(["which", packageManager], capture_output=True, text=True)

    if not result.stdout:
        print(f"{packageManager} is not found!")
        continue

    print(f"Your Package Manager is {result.stdout.strip()}")

    while True:
        packageManagerConfirm = input("... right? [Y/n] ").strip().lower()

        if packageManagerConfirm in ['', 'y', 'Y']:
            print("Alright. Let's continue...")
            with open(os.path.expanduser("~/.pkgmgr"), "w", encoding="utf-8") as file:
                file.write(f"{result.stdout.strip()}")
            break
        
        elif packageManagerConfirm == 'n' or packageManagerConfirm == 'N':
            break

        else:
            print("... right? [Y/n] ")

    if packageManagerConfirm in ['', 'y', 'Y']:
        break

print("[1/3] Installin' dependencies... ")

install_cmd = "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y"

if packageManager == "apt" or packageManager == "dnf" or packageManager == "zypper" or packageManager == "apt-get" or packageManager == "yum":
    subprocess.run(["sudo", packageManager, "install", *dependencies])
    subprocess.run(install_cmd, shell=True, check=True)
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.cargo/bin")

elif packageManager == "pacman":
    subprocess.run(["sudo", packageManager, "-S", *dependencies])
    subprocess.run(install_cmd, shell=True, check=True)
    os.environ["PATH"] += os.pathsep + os.path.expanduser("~/.cargo/bin")

print("[2/3] Clonin' & buildin' from Github...")

subprocess.run(["git", "clone", gitProjectLink], cwd=os.path.expanduser("~/.local/share"))

subprocess.run(["cargo", "build", "--release"], cwd=os.path.expanduser("~/.local/share/sysadmintools/upd"))

subprocess.run(["g++", "genpass.cpp", "-o", "genpass"], cwd=os.path.expanduser("~/.local/share/sysadmintools/genpass"))

print("[3/3] Installin' SysAdminTools to system")

dest = os.path.expanduser("~/.local/share/sysadmintools")

with open(os.path.expanduser("/tmp/alias-for-sysadmintools"), "w", encoding="utf-8") as file:
    file.write("alias upd='~/.local/share/sysadmintools/upd/target/release/upd'\n")
    file.write("alias genpass='~/.local/share/sysadmintools/genpass/genpass'\n")
    file.write("alias servicegen='~/.local/share/sysadmintools/servicegen/target/release/servicegen'\n")
    file.write("alias logclean='~/.local/share/sysadmintools/logclean/logclean.py'\n")

with open(os.path.expanduser("~/.bashrc"), "a", encoding="utf-8") as bashrc, \
     open("/tmp/alias-for-sysadmintools", "r", encoding="utf-8") as tmp:
    bashrc.write(tmp.read())


print("Installation complete! Please restart your terminal or run 'source ~/.bashrc' to apply the changes.")