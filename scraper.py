import requests

RAPIDAPI_URL = "https://jobs-search-api.p.rapidapi.com/search"
HEADERS = {
    "X-RapidAPI-Host": "jobs-search-api.p.rapidapi.com",
    "X-RapidAPI-Key": "<YOUR_RAPIDAPI_KEY>"
}

def scrape_api_jobs(query, city=""):
    params = {"keywords": query, "location": city, "page": "1"}
    resp = requests.get(RAPIDAPI_URL, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()
    jobs = []
    for job in data.get("data", [])[:30]:
        jobs.append({
            "title": job.get("title"),
            "company": job.get("company_name"),
            "link": job.get("job_url"),
            "source": job.get("source_name")
        })
    return jobs
