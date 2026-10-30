use std::env;
use std::error::Error;
use std::fs;
use std::path::PathBuf;
use std::process::{Command, ExitCode};

fn get_pkg_manager() -> Result<String, Box<dyn Error>> {
    let home = env::var("HOME")?;
    let mut path = PathBuf::from(home);
    path.push(".pkgmgr");
    let content = fs::read_to_string(&path)?;
    let pkg_manager = content.trim();
    if pkg_manager.is_empty() {
        return Err("The .pkgmgr file is empty. Run the installer again.".into());
    }
    Ok(pkg_manager.to_string())
}

fn main() -> ExitCode {
    let pkg_manager = match get_pkg_manager() {
        Ok(pkg_manager) => pkg_manager,
        Err(error) => {
            eprintln!("Could not read package manager configuration: {error}");
            return ExitCode::FAILURE;
        }
    };
    println!("I use the manager: {}", pkg_manager);

    let status = match Command::new("sudo")
        .arg(&pkg_manager)
        .arg("update")
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
