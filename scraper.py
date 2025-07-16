import requests
from bs4 import BeautifulSoup

def scrape_indeed_jobs(query, city=""):
    jobs = []
    url = f"https://pk.indeed.com/jobs?q={query.replace(' ', '+')}&l={city.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    cards = soup.select(".result") or soup.select(".tapItem")

    for card in cards:
        title = card.select_one("h2.jobTitle span")
        company = card.select_one(".companyName")
        link = card.select_one("a[href*='/rc/clk']")
        if title and link:
            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip() if company else "Unknown",
                "link": "https://pk.indeed.com" + link['href'],
                "source": "Indeed"
            })
    return jobs

def scrape_mustakbil_jobs(query, city=""):
    jobs = []
    url = f"https://www.mustakbil.com/jobs/pakistan/{city.lower().replace(' ', '-')}/{query.replace(' ', '-')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    listings = soup.select(".job-opening")

    for job in listings:
        title = job.select_one("h3.job-title a")
        company = job.select_one(".company-name")
        if title:
            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip() if company else "Unknown",
                "link": "https://www.mustakbil.com" + title['href'],
                "source": "Mustakbil"
            })
    return jobs

def scrape_all_jobs_for_students(query, city=""):
    indeed = scrape_indeed_jobs(query, city)
    mustakbil = scrape_mustakbil_jobs(query, city)
    return indeed + mustakbil
