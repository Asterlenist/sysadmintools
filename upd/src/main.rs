use std::env;
use std::fs;
use std::path::PathBuf;
use std::process::Command;

fn get_pkg_manager() -> String {
    // 1. Получаем путь к домашней папке
    let home = env::var("HOME").expect("Could not find variable HOME");
    
    // 2. Строим полный путь (home + "/.pkgmgr")
    let mut path = PathBuf::from(home);
    path.push(".pkgmgr");
    
    // 3. Читаем файл в строку. 
    // expect() уронит программу с ошибкой, если файла нет.
    let content = fs::read_to_string(&path)
        .expect("The .pkgmgr file was not found. Run the installer!");
        
    // 4. Убираем лишние пробелы и переносы строк (аналог .strip() в Python)
    content.trim().to_string()
}

fn main() {
    let pkg_manager = get_pkg_manager();
    println!("I use the manager: {}", pkg_manager);

    let status = Command::new("sudo")
        .arg(&pkg_manager)
        .arg("update")
        .status()
        .expect("Failed to run command");

    if status.success() {
        println!("The update was successful!");
    } else {
        println!("Error during update");
    }
}
