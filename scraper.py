import requests
from bs4 import BeautifulSoup

def scrape_rozee_jobs(query, location=""):
    jobs = []
    query_formatted = query.replace(' ', '-').lower()
    location_formatted = location.replace(' ', '-').lower()
    
    if location:
        url = f"https://www.rozee.pk/job-search/{query_formatted}-jobs-in-{location_formatted}"
    else:
        url = f"https://www.rozee.pk/job-search/{query_formatted}-jobs"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    job_blocks = soup.select('.job-search-list .job')
    for job in job_blocks:
        title_tag = job.select_one('.job-title a')
        if not title_tag:
            continue
        title = title_tag.get_text(strip=True)
        link = "https://www.rozee.pk" + title_tag.get('href')

        # Experience Estimation
        exp_tag = job.select_one('.job-metadata span')
        experience_text = exp_tag.get_text(strip=True) if exp_tag else "Not Mentioned"

        jobs.append({
            'title': title,
            'link': link,
            'experience_text': experience_text
        })
    
    return jobs

def filter_by_experience(jobs, level):
    level = level.lower()
    filtered = []
    for job in jobs:
        exp = job['experience_text'].lower()
        if level == 'fresh' and ("0" in exp or "fresh" in exp):
            filtered.append(job)
        elif level == 'intermediate' and any(x in exp for x in ['2', '3', '4', 'mid']):
            filtered.append(job)
        elif level == 'expert' and any(x in exp for x in ['5', '6', '7', '8', 'senior', 'expert']):
            filtered.append(job)
    return filtered if filtered else jobs  # fallback to all if none matched
