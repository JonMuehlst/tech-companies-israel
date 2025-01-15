#!/usr/bin/env python
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from tci.services.auth import auth_service


def create_admin_user():
    """Create a default admin user"""
    try:
        user = auth_service.register_user(
            email="admin@example.com", password="admin123", full_name="Admin User"
        )
        print(f"Admin user created successfully: {user.email}")
    except Exception as e:
        print(f"Error creating admin user: {e}")


if __name__ == "__main__":
    create_admin_user()
