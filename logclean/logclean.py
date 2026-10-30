import os
import time
import sys

def clean_logs(log_dir, days, dry_run=True):
    print(f"Searching for logs older than {days} days in {log_dir}...")
    
    current_time = time.time()
    cutoff_time = current_time - (days * 86400)
    total_freed_mb = 0

    for root, dirs, files in os.walk(log_dir):
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
            except Exception as e:
                print(f"Error with {file_path}: {e}")

    print(f"\nDone! {'Would have' if dry_run else 'Actually'} freed: {total_freed_mb:.2f} MB")

if __name__ == "__main__":

    if os.geteuid() != 0:
        print("Warning: Rights of root (sudo) are required to delete system logs.")
    

    delete_flag = "--delete" in sys.argv
    
    clean_logs("/var/log", days=30, dry_run=not delete_flag)