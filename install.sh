#!/usr/bin/env bash

set -euo pipefail

VERSION="v0.3"
REPOSITORY_URL="https://github.com/Asterlenist/sysadmintools"

if ! command -v sudo >/dev/null 2>&1; then
    printf "sudo is not installed. Log in as root with 'su -', then run 'apt install sudo'.\n" >&2
    exit 1
fi

printf 'Installer %s\n' "$VERSION"

if [[ ! -r /dev/tty ]]; then
    printf 'This installer requires an interactive terminal.\n' >&2
    exit 1
fi

while true; do
    read -r -p "Write your Package Manager (example: apt) " package_manager </dev/tty

    case "$package_manager" in
        apt|apt-get)
            install_action="install"
            compiler_package="g++"
            ;;
        dnf|yum|zypper)
            install_action="install"
            compiler_package="gcc-c++"
            ;;
        pacman)
            install_action="-S"
            compiler_package="gcc"
            ;;
        *)
            printf '%s is not a supported package manager.\n' "$package_manager"
            continue
            ;;
    esac

    package_manager_path="$(command -v "$package_manager" || true)"
    if [[ -z "$package_manager_path" ]]; then
        printf '%s is not found!\n' "$package_manager"
        continue
    fi

    printf 'Your Package Manager is %s\n' "$package_manager_path"

    while true; do
        read -r -p "... right? [Y/n] " package_manager_confirm </dev/tty
        package_manager_confirm="${package_manager_confirm,,}"

        case "$package_manager_confirm" in
            ""|y)
                printf "Alright. Let's continue...\n"
                break 2
                ;;
            n)
                break
                ;;
            *)
                printf '... right? [Y/n]\n'
                ;;
        esac
    done
done

printf "[1/3] Installin' dependencies...\n"
dependencies=(tree git curl "$compiler_package")
if [[ "$package_manager" == apt || "$package_manager" == apt-get ]]; then
    dependencies+=(build-essential bsdmainutils util-linux)
fi

dependency_command=(sudo "$package_manager_path" "$install_action")
if [[ "$package_manager" == pacman ]]; then
    dependency_command+=(--needed)
fi
"${dependency_command[@]}" "${dependencies[@]}"

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"

printf "[2/3] Clonin' & buildin' from Github...\n"
share_dir="$HOME/.local/share"
mkdir -p "$share_dir"
destination="$share_dir/sysadmintools"
git clone "$REPOSITORY_URL" "$destination"
cargo build --release --manifest-path "$destination/upd/Cargo.toml"
g++ -std=c++11 "$destination/genpass/genpass.cpp" -o "$destination/genpass/genpass"
g++ -std=c++11 "$destination/diskcheck/diskcheck.cc" -o "$destination/diskcheck/diskcheck"

printf "[3/3] Installin' SysAdminTools to system\n"
{
    for tool in upd genpass diskcheck; do
        printf -v alias_value '%q' "$destination/$tool/$tool"
        printf 'alias %s=%q\n' "$tool" "$alias_value"
    done

    for tool in pkgcheck sysbak sysinfo usercheck; do
        printf -v alias_value 'bash %q' "$destination/$tool/$tool.sh"
        printf 'alias %s=%q\n' "$tool" "$alias_value"
    done

    for tool in servicegen logclean; do
        printf -v alias_value 'python3 %q' "$destination/$tool/$tool.py"
        printf 'alias %s=%q\n' "$tool" "$alias_value"
    done
} >>"$HOME/.bashrc"

printf "Installation complete! Please restart your terminal or run 'source ~/.bashrc' to apply the changes.\n"