import streamlit as st
from scraper import scrape_all_jobs_for_students

st.set_page_config(page_title="🎓 Student Internship Finder", layout="centered")

st.title("🎓 Student Internship & Entry Job Finder – Pakistan")
st.markdown("Find internships and trainee positions relevant to your degree or field!")

# Input Fields
query = st.text_input("🎯 What are you looking for? (e.g. Software Intern, Marketing Trainee)")
city = st.text_input("📍 Enter City (e.g. Lahore, Islamabad)", "")

if st.button("🔍 Find Opportunities"):
    if not query:
        st.error("Please enter a job title or interest.")
    else:
        with st.spinner("Searching multiple job portals..."):
            results = scrape_all_jobs_for_students(query, city)

        if results:
            st.success(f"Found {len(results)} opportunities!")
            for job in results:
                st.markdown(f"**[{job['title']}]({job['link']})**  \n"
                            f"📍 {job['company']} — *{job['source']}*")
                st.markdown("---")
        else:
            st.warning("No internships or jobs found. Try a different keyword or city.")
