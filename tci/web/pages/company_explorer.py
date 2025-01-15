import streamlit as st

from tci.services.company import CompanyService


def show(company_service: CompanyService):
    """Show company explorer page"""
    st.title("Company Explorer")

    # Search bar
    search_query = st.text_input(
        "Search companies", placeholder="Enter company name..."
    )

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "Industry", ["All", "Software", "Hardware", "AI/ML", "Cybersecurity"]
        )
    with col2:
        st.selectbox("Size", ["All", "1-10", "11-50", "51-200", "201-1000", "1000+"])

    # Company list
    companies = company_service.get_companies()

    if not companies:
        st.info("No companies found. Companies will appear here once added.")
        return

    for company in companies:
        with st.expander(company.name):
            st.write(f"**Website:** {company.website}")
            if company.description:
                st.write(company.description)

            # Show job openings if any
            if company.jobs:
                st.subheader("Open Positions")
                for job in company.jobs:
                    st.write(f"- {job.title} ({job.location})")
