import pytest

from tci.services.auth import AuthService


def test_password_hashing():
    """Test password hashing and verification"""
    auth = AuthService()
    password = "test123"
    hashed = auth.get_password_hash(password)

    assert hashed != password
    assert auth.verify_password(password, hashed)
    assert not auth.verify_password("wrong", hashed)


def test_token_creation_and_verification(test_db):
    """Test JWT token creation and verification"""
    auth = AuthService()

    # Create a test user
    user = auth.register_user("test@example.com", "test123")
    assert user is not None

    # Create and verify token
    token = auth.create_access_token(user.id)
    assert token is not None

    verified_user = auth.verify_token(token)
    assert verified_user is not None
    assert verified_user.id == user.id

    # Test invalid token
    assert auth.verify_token("invalid-token") is None
