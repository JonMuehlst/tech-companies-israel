from functools import wraps
from typing import Any, Callable, Optional, TypeVar, cast

import streamlit as st

from tci.db.models import User
from tci.services.auth import auth_service

F = TypeVar("F", bound=Callable[..., Any])


def require_auth(func: F) -> F:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        if "user_token" not in st.session_state:
            show_login()
            return None

        # Verify token
        user: Optional[User] = auth_service.verify_token(st.session_state.user_token)
        if not user:
            show_login()
            return None

        return func(*args, **kwargs)

    return cast(F, wrapper)


def show_login() -> None:
    """Show login/register form"""
    st.title("Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        email: str = st.text_input("Email", key="login_email")
        password: str = st.text_input("Password", type="password", key="login_password")

        if st.button("Login"):
            user: Optional[User] = auth_service.authenticate_user(email, password)
            if user:
                st.session_state.user_token = auth_service.create_access_token(user.id)
                st.rerun()
            else:
                st.error("Invalid email or password")

    with tab2:
        email: str = st.text_input("Email", key="register_email")
        password: str = st.text_input(
            "Password", type="password", key="register_password"
        )
        full_name: str = st.text_input("Full Name", key="register_name")

        if st.button("Register"):
            try:
                user: User = auth_service.register_user(email, password, full_name)
                st.session_state.user_token = auth_service.create_access_token(user.id)
                st.success("Registration successful!")
                st.rerun()
            except Exception as e:
                st.error(f"Registration failed: {str(e)}")
