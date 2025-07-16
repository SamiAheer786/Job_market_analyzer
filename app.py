import streamlit as st
from scraper import scrape_indeed_jobs

st.set_page_config(page_title="Student Job Finder Debug", layout="centered")
st.title("🔍 Debugged Internship/Entry Job Finder")

query = st.text_input("Role (e.g. software intern)")
city = st.text_input("City (e.g. Lahore)", "")

if st.button("Search"):
    if not query:
        st.error("Please enter a role.")
    else:
        st.write("Searching Indeed…")
        jobs = scrape_indeed_jobs(query, city)
        st.write(f"Found {len(jobs)} raw results.")
        if jobs:
            for job in jobs:
                st.markdown(f"**[{job['title']}]({job['link']})** — {job['company']}")
        else:
            st.warning("No opportunities found — check debug logs or try other keywords.")
