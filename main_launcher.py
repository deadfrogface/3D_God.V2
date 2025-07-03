import subprocess
import sys
import os

def main():
    script = os.path.join(os.path.dirname(__file__), "main.py")
    if not os.path.isfile(script):
        print("main.py not found. Please ensure it exists in the same directory as this launcher.")
        sys.exit(1)

    # Launch main.py with the same Python interpreter
    result = subprocess.run([sys.executable, script] + sys.argv[1:])
    sys.exit(result.returncode)

if __name__ == "__main__":
    main()
