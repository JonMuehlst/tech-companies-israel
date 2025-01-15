from pathlib import Path

import streamlit.web.bootstrap as bootstrap


def main():
    app_path = str(Path(__file__).parent / "tci" / "web" / "app.py")
    bootstrap.run(app_path, "", [], {})
