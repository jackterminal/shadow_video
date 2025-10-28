import os
import subprocess
import sys

def install_dependencies():
    """Installs dependencies from requirements.txt."""
    print("Installing dependencies for ComfyUI-ShadowVideo...")
    
    # Get the directory where this script is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(current_dir, "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print(f"Error: requirements.txt not found at {requirements_path}")
        return

    # Use the same python executable that is running this script
    python_executable = sys.executable
    
    try:
        subprocess.check_call([python_executable, "-m", "pip", "install", "-r", requirements_path])
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        print("Please try installing manually using:")
        print(f"{python_executable} -m pip install -r {requirements_path}")

if __name__ == "__main__":
    install_dependencies()

