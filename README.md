# SysAdminTools

SysAdminTools is a small collection of command-line utilities and experiments
for Linux system administration. The tools are independent and can be built or
run separately.

## Tools

| Tool | Description |
| --- | --- |
| `genpass` | Generates a 16-character password using uppercase letters, lowercase letters, digits, and special characters. Its length and character sets are currently configured in the source code. |
| `upd` | Runs the `update` command for the package manager recorded in `~/.pkgmgr`, using `sudo`. |
| `servicegen` | Interactively collects values for a systemd service unit and prints a draft along with installation commands. It does not create or install the unit file. |
| `logclean` | Scans `/var/log` for `.log` and `.gz` files older than 30 days, skipping paths containing `journal`. It previews deletions by default. |
| `install.py` | An experimental interactive installer. It installs dependencies, installs Rust, clones this repository, builds some tools, and appends aliases to `~/.bashrc`. See the notes below before running it. |

## Requirements

- Linux
- Python 3 for `servicegen` and `logclean`
- A C++ compiler such as `g++` for `genpass`
- Rust and Cargo for `upd`
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

### Package updater

Build and run:

```sh
cd upd
cargo build --release
```

The program expects `~/.pkgmgr` to contain the name of an installed package
manager, such as `apt` or `dnf`. For example:

```sh
printf '%s\n' apt > ~/.pkgmgr
cargo run --release
```

`upd` runs `sudo <package-manager> update`; it does not install available
upgrades.

### Service unit draft

```sh
python3 servicegen/servicegen.py
```

Review the printed draft before using it. The script prints prompts' answers
as a draft; it does not validate values or write a unit file.

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

## Installer notes

`install.py` is not required to use the tools. It prompts for a package manager,
uses `sudo` to install dependencies, downloads and runs the Rust installer,
clones the repository into `~/.local/share/sysadmintools`, and appends aliases
to `~/.bashrc`. Review the script before running it, since it makes system and
shell configuration changes.

The installer is experimental: it builds `upd` and `genpass`, but does not
build or install `servicegen` or `logclean`. The manual commands above are the
reliable way to run those scripts.

## License

This project is distributed under the [BSD 2-Clause License](./LICENSE).