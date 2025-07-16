from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def scrape_indeed_jobs(query, city=""):
    options = Options()
    options.add_argument("--headless")  # run without browser window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    url = f"https://pk.indeed.com/jobs?q={query.replace(' ', '+')}&l={city.replace(' ', '+')}"
    driver.get(url)
    time.sleep(5)  # let page load fully

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    jobs = []
    cards = soup.select(".job_seen_beacon")  # new class for job card
    for card in cards:
        title_el = card.select_one("h2.jobTitle span")
        company_el = card.select_one(".companyName")
        link_el = card.find("a", href=True)
        if title_el and link_el:
            jobs.append({
                "title": title_el.text.strip(),
                "company": company_el.text.strip() if company_el else "Unknown",
                "link": "https://pk.indeed.com" + link_el['href'],
                "source": "Indeed"
            })
    return jobs
