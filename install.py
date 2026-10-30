import os
import shlex
import shutil
import subprocess

VERSION = "v0.1"
REPOSITORY_URL = "https://github.com/Asterlenist/sysadmintools"
PACKAGE_MANAGERS = {
    "apt": ("install", "g++"),
    "apt-get": ("install", "g++"),
    "dnf": ("install", "gcc-c++"),
    "yum": ("install", "gcc-c++"),
    "zypper": ("install", "gcc-c++"),
    "pacman": ("-S", "gcc"),
}

print("Installer ", VERSION)

while True:
    package_manager = input("Write your Package Manager (example: apt) ").strip()
    if package_manager not in PACKAGE_MANAGERS:
        print(f"{package_manager} is not a supported package manager.")
        continue

    package_manager_path = shutil.which(package_manager)
    if package_manager_path is None:
        print(f"{package_manager} is not found!")
        continue

    print(f"Your Package Manager is {package_manager_path}")

    while True:
        package_manager_confirm = input("... right? [Y/n] ").strip().lower()

        if package_manager_confirm in ("", "y"):
            print("Alright. Let's continue...")
            with open(os.path.expanduser("~/.pkgmgr"), "w", encoding="utf-8") as file:
                file.write(package_manager_path)
            break

        if package_manager_confirm == "n":
            break

        print("... right? [Y/n] ")

    if package_manager_confirm in ("", "y"):
        break

try:
    print("[1/3] Installin' dependencies... ")
    install_action, compiler_package = PACKAGE_MANAGERS[package_manager]
    dependency_command = ["sudo", package_manager, install_action]
    if package_manager == "pacman":
        dependency_command.append("--needed")
    subprocess.run(
        [*dependency_command, "tree", "git", "curl", compiler_package],
        check=True,
    )

    rustup_download = subprocess.run(
        [
            "curl",
            "--proto",
            "=https",
            "--tlsv1.2",
            "-sSf",
            "https://sh.rustup.rs",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    subprocess.run(
        ["sh", "-s", "--", "-y"],
        input=rustup_download.stdout,
        text=True,
        check=True,
    )

    cargo_bin = os.path.expanduser("~/.cargo/bin")
    os.environ["PATH"] = os.pathsep.join((os.environ.get("PATH", ""), cargo_bin))

    print("[2/3] Clonin' & buildin' from Github...")
    share_dir = os.path.expanduser("~/.local/share")
    os.makedirs(share_dir, exist_ok=True)
    dest = os.path.join(share_dir, "sysadmintools")
    subprocess.run(["git", "clone", REPOSITORY_URL, dest], check=True)
    subprocess.run(
        ["cargo", "build", "--release"],
        cwd=os.path.join(dest, "upd"),
        check=True,
    )
    subprocess.run(
        ["g++", "-std=c++11", "genpass.cpp", "-o", "genpass"],
        cwd=os.path.join(dest, "genpass"),
        check=True,
    )

    print("[3/3] Installin' SysAdminTools to system")
    commands = {
        "upd": os.path.join(dest, "upd", "target", "release", "upd"),
        "genpass": os.path.join(dest, "genpass", "genpass"),
        "servicegen": f"python3 {os.path.join(dest, 'servicegen', 'servicegen.py')}",
        "logclean": f"python3 {os.path.join(dest, 'logclean', 'logclean.py')}",
    }
    with open(os.path.expanduser("~/.bashrc"), "a", encoding="utf-8") as bashrc:
        for alias, command in commands.items():
            bashrc.write(f"alias {alias}={shlex.quote(command)}\n")

except (OSError, subprocess.CalledProcessError) as error:
    raise SystemExit(f"Installation failed: {error}") from error

print("Installation complete! Please restart your terminal or run 'source ~/.bashrc' to apply the changes.")