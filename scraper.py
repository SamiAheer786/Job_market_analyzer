import requests
from bs4 import BeautifulSoup

def scrape_indeed_jobs(query, location=""):
    jobs = []
    query_formatted = query.replace(" ", "+")
    location_formatted = location.replace(" ", "+")
    url = f"https://pk.indeed.com/jobs?q={query_formatted}&l={location_formatted}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    job_cards = soup.select(".result") or soup.select(".tapItem")
    for card in job_cards:
        title_tag = card.select_one("h2.jobTitle span")
        title = title_tag.text.strip() if title_tag else "No Title"

        link_tag = card.find("a", href=True)
        if link_tag and "/rc/clk" in link_tag["href"]:
            link = "https://pk.indeed.com" + link_tag["href"]
        else:
            continue

        company_tag = card.select_one(".companyName")
        company = company_tag.text.strip() if company_tag else "Unknown Company"

        jobs.append({
            "title": f"{title} at {company}",
            "link": link,
            "experience_text": "Not Mentioned"
        })

    return jobs

def filter_by_experience(jobs, level):
    # Since Indeed doesn't provide experience data on search pages,
    # skip filtering and return all jobs
    return jobs
