import subprocess
import sys
import importlib

REQUIRED_PACKAGES = [
    "flask",
    "torch",
    "transformers",
    "requests"
]

def ensure_dependencies():
    for package in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"📦 Installiere fehlendes Paket: {package}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
