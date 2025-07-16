import requests
from bs4 import BeautifulSoup

def scrape_indeed_jobs(query, city=""):
    jobs = []
    url = f"https://pk.indeed.com/jobs?q={query.replace(' ', '+')}&l={city.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}

    res = requests.get(url, headers=headers)
    print(f"[DEBUG] GET {url} → {res.status_code}")
    soup = BeautifulSoup(res.text, 'html.parser')

    cards = soup.select(".tapItem") + soup.select(".result")
    print(f"[DEBUG] Found {len(cards)} job cards")

    for card in cards:
        title_el = card.select_one("h2.jobTitle span")
        company_el = card.select_one(".companyName")
        link_el = card.select_one("a[href*='/rc/clk']")
        if title_el and link_el:
            jobs.append({
                "title": title_el.text.strip(),
                "company": company_el.text.strip() if company_el else "Unknown",
                "link": "https://pk.indeed.com" + link_el['href'],
                "source": "Indeed"
            })

    print(f"[DEBUG] Parsed {len(jobs)} job entries")
    return jobs
