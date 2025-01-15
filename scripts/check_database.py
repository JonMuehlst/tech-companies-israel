#!/usr/bin/env python
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from sqlalchemy import inspect

from tci.core.config import settings
from tci.db.postgresql import engine


def check_database():
    """Check database connection and list all tables"""
    inspector = inspect(engine)

    print(f"Checking database connection to: {settings.POSTGRES_URL}")
    print("\nExisting tables:")
    for table_name in inspector.get_table_names():
        print(f"- {table_name}")
        # Print columns for each table
        for column in inspector.get_columns(table_name):
            print(f"  - {column['name']}: {column['type']}")


if __name__ == "__main__":
    check_database()
