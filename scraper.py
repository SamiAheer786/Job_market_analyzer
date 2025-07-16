import requests
from bs4 import BeautifulSoup

# 🔹 1. INDEED.COM.PK
def scrape_indeed_jobs(query, location=""):
    jobs = []
    url = f"https://pk.indeed.com/jobs?q={query.replace(' ', '+')}&l={location.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    cards = soup.select(".result") or soup.select(".tapItem")
    for card in cards:
        title = card.select_one("h2.jobTitle span")
        company = card.select_one(".companyName")
        link_tag = card.find("a", href=True)
        if title and link_tag:
            jobs.append({
                "title": title.text.strip(),
                "company": company.text.strip() if company else "Unknown",
                "link": "https://pk.indeed.com" + link_tag['href'],
                "source": "Indeed"
            })
    return jobs


# 🔹 2. MUSTAKBIL.COM
def scrape_mustakbil_jobs(query, location=""):
    jobs = []
    url = f"https://www.mustakbil.com/jobs/pakistan/{location.lower().replace(' ', '-')}/{query.replace(' ', '-')}"
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


# 🔹 3. INTERNS.PK
def scrape_interns_pk():
    jobs = []
    url = "https://www.interns.pk/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    articles = soup.select(".card-body")
    for a in articles:
        title_tag = a.select_one("h5.card-title a")
        if title_tag:
            jobs.append({
                "title": title_tag.text.strip(),
                "company": "Interns.pk Listing",
                "link": title_tag['href'],
                "source": "Interns.pk"
            })
    return jobs


# 🔹 COMBINE RESULTS
def scrape_all_jobs_for_students(query, city):
    indeed = scrape_indeed_jobs(query, city)
    mustakbil = scrape_mustakbil_jobs(query, city)
    interns = scrape_interns_pk() if "intern" in query.lower() else []
    return indeed + mustakbil + interns
