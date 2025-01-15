#!/usr/bin/env python
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from tci.db.init_db import init_database

if __name__ == "__main__":
    init_database()
