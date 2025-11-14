import subprocess
import sys

print("Installing dependencies...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
print("✓ Dependencies installed successfully!")
print("\nYou can now run: python browser.py")
