import os
import subprocess
import sys

def run_command(command):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error running {command}")
        return False
    return True

def main():
    print("=== Neural Network Art Classifier Pipeline ===")
    
    # Step 1: Install dependencies
    print("\n[Step 1] Checking/Installing dependencies...")
    run_command(f"{sys.executable} -m pip install -r requirements.txt")
    
    # Step 2: Download Data
    print("\n[Step 2] Collecting Data...")
    # Using python to run the script
    run_command(f"{sys.executable} data_collector.py")
    
    # Step 3: Train Model
    print("\n[Step 3] Training Model...")
    run_command(f"{sys.executable} train_model.py")
    
    # Step 4: GitHub Sync
    print("\n[Step 4] Pushing results to GitHub...")
    run_command("git add .")
    run_command("git commit -m 'Auto-update: Overnight training results'")
    run_command("git push")
    
    print("\n[DONE] Pipeline completed.")
    
    print("Waiting 10 minutes to ensure upload completes...")
    import time
    time.sleep(600) # 600 seconds = 10 minutes
    
    print("Shutting down the PC now...")
    # Windows Shutdown Command
    os.system("shutdown /s /t 10") # 10 seconds warning before shutdown

if __name__ == "__main__":
    main()
