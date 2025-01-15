import sys
from pathlib import Path
from typing import Optional

import streamlit as st

from tci.core.config import settings
from tci.services.company import CompanyService, company_service
from tci.services.jobs import JobService, job_service
from tci.web import pages
from tci.web.auth import require_auth


class TechCompaniesApp:
    def __init__(self) -> None:
        self.setup_session_state()
        self.initialize_services()

    def initialize_services(self) -> None:
        """Initialize required services"""
        # Services are imported and initialized at module level
        pass

    def setup_session_state(self) -> None:
        """Initialize session state variables"""
        if "page" not in st.session_state:
            st.session_state.page = "Companies"

    @require_auth
    def run(self) -> None:
        st.set_page_config(page_title="Israeli Tech Companies", layout="wide")

        """Main app entry point"""
        st.sidebar.title("Israeli Tech Explorer")
        st.write("Coming soon: Explore the Israeli tech ecosystem!")

        if st.sidebar.button("Logout"):
            del st.session_state.user_token
            st.experimental_rerun()

        # Navigation
        st.sidebar.title("Navigation")
        st.sidebar.info("This is a work in progress. Stay tuned!")
        page: str = st.sidebar.selectbox(
            "Navigate to", ["Companies", "Jobs", "Analytics", "ML Insights"]
        )

        # Page routing
        if page == "Companies":
            pages.company_explorer.show(company_service)
        elif page == "Jobs":
            pages.job_board.show(job_service)
        elif page == "Analytics":
            pages.analytics.show(company_service, job_service)
        else:
            pages.ml_insights.show(company_service, job_service)


def main() -> None:
    app: TechCompaniesApp = TechCompaniesApp()
    app.run()


if __name__ == "__main__":
    main()
