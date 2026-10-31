import os
import shlex
import shutil
import subprocess

if shutil.which("sudo") is None:
    raise SystemExit(
        "sudo is not installed. Log in as root with 'su -', then run 'apt install sudo'."
    )

VERSION = "v0.31"
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


def clone_or_pull_repository(repository_url: str, destination: str) -> None:
    if os.path.exists(destination):
        repository_check = subprocess.run(
            ["git", "-C", destination, "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=False,
        )
        if (
            repository_check.returncode != 0
            or repository_check.stdout.strip() != "true"
        ):
            raise RuntimeError(
                f"Destination exists but is not a Git repository: {destination}"
            )
        subprocess.run(["git", "-C", destination, "pull"], check=True)
    else:
        subprocess.run(["git", "clone", repository_url, destination], check=True)


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
            break

        if package_manager_confirm == "n":
            break

        print("... right? [Y/n] ")

    if package_manager_confirm in ("", "y"):
        break

try:
    print("[1/3] Installin' dependencies... ")
    install_action, compiler_package = PACKAGE_MANAGERS[package_manager]
    dependencies = ["tree", "git", "curl", compiler_package]
    if package_manager in ("apt", "apt-get"):
        dependencies.extend(["build-essential", "bsdmainutils", "util-linux"])

    dependency_command = ["sudo", package_manager_path, install_action]
    if package_manager == "pacman":
        dependency_command.append("--needed")
    subprocess.run(
        [*dependency_command, *dependencies],
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
    clone_or_pull_repository(REPOSITORY_URL, dest)
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
    subprocess.run(
        ["g++", "-std=c++11", "diskcheck.cc", "-o", "diskcheck"],
        cwd=os.path.join(dest, "diskcheck"),
        check=True,
    )

    print("[3/3] Installin' SysAdminTools to system")
    commands = {
        "upd": os.path.join(dest, "upd", "target", "release", "upd"),
        "genpass": os.path.join(dest, "genpass", "genpass"),
        "diskcheck": os.path.join(dest, "diskcheck", "diskcheck"),
        "pkgcheck": f"bash {os.path.join(dest, 'pkgcheck', 'pkgcheck.sh')}",
        "servicegen": f"python3 {os.path.join(dest, 'servicegen', 'servicegen.py')}",
        "logclean": f"python3 {os.path.join(dest, 'logclean', 'logclean.py')}",
        "sysbak": f"bash {os.path.join(dest, 'sysbak', 'sysbak.sh')}",
        "sysinfo": f"bash {os.path.join(dest, 'sysinfo', 'sysinfo.sh')}",
        "usercheck": f"bash {os.path.join(dest, 'usercheck', 'usercheck.sh')}",
    }
    with open(os.path.expanduser("~/.bashrc"), "a", encoding="utf-8") as bashrc:
        for alias, command in commands.items():
            bashrc.write(f"alias {alias}={shlex.quote(command)}\n")

except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
    raise SystemExit(f"Installation failed: {error}") from error

print("Installation complete! Please restart your terminal or run 'source ~/.bashrc' to apply the changes.")