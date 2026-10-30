import argparse
import os
import time

def clean_logs(log_dir, days, dry_run=True):
    print(f"Searching for logs older than {days} days in {log_dir}...")
    
    current_time = time.time()
    cutoff_time = current_time - (days * 86400)
    total_freed_mb = 0
    error_count = 0

    def report_walk_error(error):
        nonlocal error_count
        error_count += 1
        print(f"Error scanning {error.filename}: {error}")

    for root, _dirs, files in os.walk(log_dir, onerror=report_walk_error):
        if "journal" in root:
            continue
            
        for file in files:
            if not (file.endswith(".log") or file.endswith(".gz")):
                continue
                
            file_path = os.path.join(root, file)
            
            try:
                file_mtime = os.path.getmtime(file_path)
                if file_mtime < cutoff_time:
                    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    
                    if dry_run:
                        print(f"[EXAMPLE] Would delete: {file_path} ({file_size_mb:.2f} MB)")
                    else:
                        os.remove(file_path)
                        print(f"Deleted: {file_path} ({file_size_mb:.2f} MB)")
                    
                    total_freed_mb += file_size_mb
            except OSError as error:
                error_count += 1
                print(f"Error with {file_path}: {error}")

    print(f"\nDone! {'Would have' if dry_run else 'Actually'} freed: {total_freed_mb:.2f} MB")
    if error_count:
        print(f"Encountered {error_count} error(s).")
    return error_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Preview or delete old log files.")
    parser.add_argument(
        "--delete",
        action="store_true",
        help="permanently delete eligible files instead of previewing them",
    )
    args = parser.parse_args()

    if args.delete and os.geteuid() != 0:
        print("Warning: Rights of root (sudo) are required to delete system logs.")

    if clean_logs("/var/log", days=30, dry_run=not args.delete):
        raise SystemExit(1)