import streamlit as st
from scraper import scrape_api_jobs

st.set_page_config(page_title="🎓 Intern & Entry Job Finder (API)", layout="centered")
st.title("🎓 Student Internship & Entry Job Finder – Pakistan")
st.markdown("Now powered by a reliable API—works smoothly everywhere!")

query = st.text_input("🎯 Role/Field (e.g. Software Intern)")
city = st.text_input("📍 City (e.g. Lahore)", "")

if st.button("🔍 Search Opportunities"):
    if not query:
        st.error("Please enter a role/field.")
    else:
        with st.spinner("Fetching jobs via API..."):
            try:
                results = scrape_api_jobs(query, city)
            except Exception as e:
                st.error(f"API error: {e}")
                results = []

        if results:
            st.success(f"✅ Found {len(results)} opportunities!")
            for job in results:
                st.markdown(f"**[{job['title']}]({job['link']})**  \n"
                            f"🏢 {job['company']} • *Source: {job['source']}*")
                st.markdown("---")
        else:
            st.warning("No opportunities found—try adjusting keyword or city.")
