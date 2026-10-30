# SysAdminTools

SysAdminTools is a small collection of command-line utilities and experiments
for Linux system administration. The tools are independent and can be built or
run separately.

## Tools

| Tool | Description |
| --- | --- |
| `genpass` | Generates a 16-character password using uppercase letters, lowercase letters, digits, and special characters. Its length and character sets are currently configured in the source code. |
| `upd` | Detects a supported package manager in `PATH` and runs its update command using `sudo`. |
| `diskcheck` | Displays disk usage by running `df -h`. |
| `pkgcheck` | Shows installed packages, available APT updates and sources, and interactively looks up package metadata. It supports Debian-based systems with APT/dpkg only. |
| `servicegen` | Interactively collects values for a systemd service unit and prints a draft along with installation commands. It does not create or install the unit file. |
| `logclean` | Scans `/var/log` for `.log` and `.gz` files older than 30 days, skipping paths containing `journal`. It previews deletions by default. |
| `sysbak` | Creates a timestamped compressed backup of `/etc`, `/var/log`, and selected user configuration files under `~/`. It skips missing optional paths instead of failing the archive. |
| `sysinfo` | Prints basic system, CPU, memory, disk, and network-interface information. |
| `usercheck` | Prints information about the current user, including groups, processes, login history, environment variables, and home-directory permissions. |
| `install.py` | An experimental interactive installer. It installs dependencies, installs Rust, clones this repository, builds some tools, and appends aliases to `~/.bashrc`. See the notes below before running it. |

## Requirements

- Linux
- Python 3 for `servicegen`, `logclean`, and `install.py`
- A C++ compiler such as `g++` for `genpass`
- A C++ compiler such as `g++` for `diskcheck`
- Rust and Cargo for `upd`
- Bash and common Linux command-line utilities for the shell scripts
- A Debian-based system with `apt` and `dpkg` for `pkgcheck`
- `sudo` and the relevant package manager to run `upd` or delete system logs

## Build and run

### Password generator

From the repository root:

```sh
g++ -std=c++11 genpass/genpass.cpp -o genpass
./genpass
```

The generator currently uses C++'s Mersenne Twister (`std::mt19937`), which is
not a cryptographic random-number generator. Do not rely on it for passwords
that require cryptographic strength.

### Disk usage

Compile and run:

```sh
g++ -std=c++11 diskcheck/diskcheck.cc -o diskcheck
./diskcheck
```

This prints the output of `df -h`.

### Package updater

Build and run:

```sh
cd upd
cargo build --release
```

The compiled executable is `upd/target/release/upd`.
The program detects the first supported package manager found in `PATH`
(`apt`, `apt-get`, `dnf`, `yum`, `zypper`, or `pacman`). For example:

```sh
cargo run --release
```

`upd` runs the package manager's update command using `sudo`; the exact effect
depends on the package manager. For example, `apt update` refreshes package
indexes, while `pacman -Syu` also installs available upgrades.

### Package information

```sh
bash pkgcheck/pkgcheck.sh
```

This script uses `dpkg` and APT commands, so it is intended for Debian-based
systems. It interactively asks for package names to display dependency,
conflict, and vulnerability-related package metadata; it is not a security
vulnerability scanner.

### Service unit draft

```sh
python3 servicegen/servicegen.py
```

Review the printed draft before using it. The script prints prompts' answers
using systemd unit-file syntax; it does not validate values or write a unit file.

### Log cleaner

Preview eligible files without deleting them:

```sh
python3 logclean/logclean.py
```

To delete matching files, pass `--delete` and run with sufficient permissions:

```sh
sudo python3 logclean/logclean.py --delete
```

Deletion is permanent. The script uses a fixed 30-day threshold and scans
`/var/log`; it does not accept a directory or age as command-line options.
Inspect the preview and ensure you have backups before using `--delete`.

### System and user information

```sh
bash sysinfo/sysinfo.sh
bash usercheck/usercheck.sh
```

`usercheck` prints environment variables and other account details; review the
output before sharing it.

### System backup

```sh
sudo bash sysbak/sysbak.sh
```

The script creates a timestamped tar.gz archive under
`$HOME/backups/sysbak`, where `$HOME` is the home directory of the user running
the script. With `sudo`, this may be root's home directory. The script skips
optional user config files that are not present.

## Installer notes

`install.py` is not required to use the tools. It prompts for a package manager,
uses `sudo` to install dependencies (including a C++ compiler), downloads and
runs the Rust installer, clones the repository into
`~/.local/share/sysadmintools`, builds `upd`, `genpass`, and `diskcheck`, and
appends aliases for all command-line tools to `~/.bashrc`. It stops if an
installation, clone, or build command fails. Review the script before running
it, since it makes system and shell configuration changes.

The installer is experimental and expects the destination repository not to
already exist. The manual commands above are also available if you prefer not
to run it.

## License

This project is distributed under the [BSD 2-Clause License](./LICENSE).