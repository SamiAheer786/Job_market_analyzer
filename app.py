import streamlit as st
from scraper import scrape_rozee_jobs, filter_by_experience

st.set_page_config(page_title="Job Market Analyzer", layout="centered")

st.title("🎯 Job Market Analyzer – Pakistan Edition")
st.markdown("Find the latest job opportunities based on your skills and experience level.")

# Input Section
job_query = st.text_input("🔍 Enter Job Title or Keywords", placeholder="e.g. Data Analyst")
experience = st.selectbox("📊 Select Experience Level", ["Fresh", "Intermediate", "Expert"])
location = st.text_input("📍 Location (Optional)", placeholder="e.g. Lahore, Karachi")

if st.button("Search Jobs"):
    if not job_query:
        st.warning("Please enter a job title or keyword.")
    else:
        with st.spinner("Fetching jobs..."):
            results = scrape_rozee_jobs(job_query, location)
            filtered_jobs = filter_by_experience(results, experience)
        
        if filtered_jobs:
            st.success(f"Found {len(filtered_jobs)} relevant jobs")
            for job in filtered_jobs:
                st.markdown(f"**[{job['title']}]({job['link']})**")
                st.caption(f"Experience: {job['experience_text']}")
        else:
            st.warning("No jobs found matching your criteria. Try adjusting your search.")
