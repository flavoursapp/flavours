import os
import platform

BASE_DIR = os.path.dirname(__file__)

WIN = platform.system() == "Windows"
MAC = platform.system() == "Darwin"
LINUX = platform.system() == "Linux"

# To be filled by app.py
app = None
working_directory = None
