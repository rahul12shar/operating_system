import subprocess
import sys

scripts = [
    "process_control.py",
    "file_management.py",
    "threading_sync.py",
    "memory_management.py",
    "device_io.py"
]

for script in scripts:
    print(f"\n{'='*60}")
    print(f"Running: {script}")
    print('='*60)
    subprocess.run([sys.executable, script])
    input("\nPress Enter to continue...")
    