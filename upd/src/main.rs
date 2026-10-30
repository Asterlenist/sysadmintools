use std::env;
use std::io;
use std::os::unix::fs::PermissionsExt;
use std::path::PathBuf;
use std::process::{Command, ExitCode};

struct PackageManager {
    name: &'static str,
    executable: PathBuf,
    args: &'static [&'static str],
}

const PACKAGE_MANAGERS: &[(&str, &[&str])] = &[
    ("apt", &["update"]),
    ("apt-get", &["update"]),
    ("dnf", &["update"]),
    ("yum", &["update"]),
    ("zypper", &["update"]),
    ("pacman", &["-Syu"]),
];

fn find_package_manager() -> io::Result<PackageManager> {
    let path = env::var_os("PATH").unwrap_or_default();
    for (name, args) in PACKAGE_MANAGERS {
        for directory in env::split_paths(&path) {
            let executable = directory.join(name);
            if executable.is_file() && executable.metadata()?.permissions().mode() & 0o111 != 0 {
                return Ok(PackageManager {
                    name,
                    executable,
                    args,
                });
            }
        }
    }

    Err(io::Error::new(
        io::ErrorKind::NotFound,
        "no supported package manager found in PATH",
    ))
}

fn main() -> ExitCode {
    let package_manager = match find_package_manager() {
        Ok(package_manager) => package_manager,
        Err(error) => {
            eprintln!("Could not find a supported package manager: {error}");
            return ExitCode::FAILURE;
        }
    };
    println!("Using package manager: {}", package_manager.name);

    let status = match Command::new("sudo")
        .arg(&package_manager.executable)
        .args(package_manager.args)
        .status()
    {
        Ok(status) => status,
        Err(error) => {
            eprintln!("Failed to run sudo or package manager: {error}");
            return ExitCode::FAILURE;
        }
    };

    if status.success() {
        println!("The update was successful!");
        ExitCode::SUCCESS
    } else {
        eprintln!("Error during update");
        ExitCode::FAILURE
    }
}
