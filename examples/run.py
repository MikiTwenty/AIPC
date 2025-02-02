import sys
import os

# Ensure the 'src' directory is in the Python path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(BASE_DIR, '../src')  # Adjust to point to your 'src' directory
sys.path.append(SRC_DIR)

from aipc import app

app.run(debug=True)