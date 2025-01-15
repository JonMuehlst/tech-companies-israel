def scrape_job_openings(url, selectors=None):
    """
    Scrapes job openings from a company's career page or job board.

    Args:
        url: The URL of the job listings page
        selectors: Dictionary of CSS selectors for different elements. If None, uses defaults.
            Expected format:
            {
                'job_container': 'div.job-posting',
                'title': 'h3.job-title',
                'department': 'div.department',
                'location': 'div.location',
                'description': 'div.job-description',
                'apply_link': 'a.apply-button'
            }

    Returns:
        A pandas DataFrame with job opening data.

    Raises:
        requests.RequestException: If the URL cannot be accessed
        ValueError: If required selectors are missing or invalid
    """
    default_selectors = {
        "job_container": "div.job-posting",
        "title": "h3.job-title",
        "department": "div.department",
        "location": "div.location",
        "description": "div.job-description",
        "apply_link": "a.apply-button",
    }
    selectors = selectors or default_selectors

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        jobs = []
        job_elements = soup.select(selectors["job_container"])

        for job in job_elements:
            job_data = {}

            # Dynamically extract data based on selectors
            for field, selector in selectors.items():
                if field == "job_container":
                    continue

                element = job.select_one(selector)
                if element:
                    if field == "apply_link":
                        job_data[field] = element.get("href", "")
                    else:
                        job_data[field] = element.text.strip()
                else:
                    job_data[field] = None

            # Add metadata
            job_data["source_url"] = url
            job_data["scraped_date"] = datetime.now().isoformat()
            jobs.append(job_data)

        return pd.DataFrame(jobs)

    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error parsing job data: {str(e)}")
