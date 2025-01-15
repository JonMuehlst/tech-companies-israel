def scrape_startup_database(url, selectors=None):
    """
    Scrapes a startup database for company information using customizable selectors.

    Args:
        url: The URL of the startup database.
        selectors: Dictionary of CSS selectors for different elements. If None, uses defaults.
            Expected format:
            {
                'company_container': 'div.portfolio-company',
                'name': 'h3.company-name',
                'description': 'p.company-description',
                'website': 'a.company-website'
            }

    Returns:
        A pandas DataFrame with company data.

    Raises:
        requests.RequestException: If the URL cannot be accessed
        ValueError: If required selectors are missing or invalid
    """
    # Use default selectors if none provided
    default_selectors = {
        "company_container": "div.portfolio-company",
        "name": "h3.company-name",
        "description": "p.company-description",
        "website": "a.company-website",
    }
    selectors = selectors or default_selectors

    # ... existing imports ...

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        companies = []
        company_elements = soup.select(selectors["company_container"])

        for company in company_elements:
            company_data = {}

            # Dynamically extract data based on selectors
            for field, selector in selectors.items():
                if field == "company_container":
                    continue

                element = company.select_one(selector)
                if element:
                    company_data[field] = (
                        element.text.strip()
                        if field != "website"
                        else element.get("href", "")
                    )
                else:
                    company_data[field] = None

            # Add source URL or domain as reference
            company_data["source_url"] = url
            companies.append(company_data)

        return pd.DataFrame(companies)

    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing data: {str(e)}")
