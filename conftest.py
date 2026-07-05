import os
import sys

# Ensure the project root (where pawpal_system.py lives) is importable,
# no matter which directory pytest is launched from.
sys.path.insert(0, os.path.dirname(__file__))
