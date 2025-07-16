import streamlit as st
from scraper import scrape_all_jobs_for_students

st.set_page_config(page_title="🎓 Student Internship Finder", layout="centered")
st.title("🎓 Student Internship & Fresh Job Finder – Pakistan")
st.markdown("Designed for students—search internships, trainee roles & fresh graduate jobs!")

query = st.text_input("🎯 Role or Field (e.g. Software Intern, Marketing Trainee)")
city = st.text_input("📍 City (Optional - e.g. Lahore, Karachi)")

if st.button("🔍 Search Opportunities"):
    if not query:
        st.error("Please enter a role or field.")
    else:
        with st.spinner("🔎 Searching multiple portals..."):
            results = scrape_all_jobs_for_students(query, city)

        if results:
            st.success(f"✅ Found {len(results)} opportunities!")
            for job in results:
                st.markdown(
                    f"**[{job['title']}]({job['link']})**  \n"
                    f"🏢 {job['company']} • *Source: {job['source']}*"
                )
                st.markdown("---")
        else:
            st.warning("😓 No opportunities found. Try adjusting keyword or city.")
