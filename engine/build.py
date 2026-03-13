import PyInstaller.__main__
import os
import sys

# Define the absolute path to the main Python script
script_path = os.path.abspath("local_ai_server.py")

# Ensure the script is run from the /engine directory
if not os.path.exists(script_path):
    print("Error: local_ai_server.py not found. Run this script from the /engine directory.")
    sys.exit(1)

print("[Builder] Starting PyInstaller compilation for Hybrid Compute Engine...")

# PyInstaller configuration
PyInstaller.__main__.run([
    script_path,
    '--name=local_ai_server', # Output executable name
    '--onefile',              # Package everything into a single executable file
    '--noconsole',            # Run in background (no CMD window pop-up for the user)
    '--clean',                # Clean PyInstaller cache before building
    
    # Hidden imports for FastAPI and Uvicorn (PyInstaller sometimes misses these)
    '--hidden-import=uvicorn',
    '--hidden-import=fastapi',
    '--hidden-import=pydantic',
    
    # MediaPipe requires its models to be bundled as data
    # (Adjust the mediapipe path depending on your virtual environment)
    '--add-data=env/Lib/site-packages/mediapipe/modules;mediapipe/modules' 
])

print("[Builder] Compilation complete! Check the /dist folder for the executable.")
