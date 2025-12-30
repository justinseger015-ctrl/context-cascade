"""
Pytest configuration for cognitive-architecture tests.

Sets up the Python path for importing core modules.
"""

import sys
from pathlib import Path

# Add the cognitive-architecture directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Tell pytest to ignore the root __init__.py as a test file
collect_ignore = ["__init__.py"]
