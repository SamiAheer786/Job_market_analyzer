import streamlit as st
from scraper import scrape_all_jobs_for_students

st.set_page_config(page_title="🎓 Student Finder", layout="centered")
st.title("🎓 Student Internship & Entry Job Finder – Pakistan")
st.markdown("Ideal for students: internships, trainee roles, fresh graduate positions!")

query = st.text_input("🎯 Role/Field (e.g. Software Intern, Marketing)")
city = st.text_input("📍 City (e.g. Lahore, Karachi)", "")

if st.button("🔍 Search"):
    if not query:
        st.error("Please enter a role or field.")
    else:
        with st.spinner("Searching..."):
            results = scrape_all_jobs_for_students(query, city)

        if results:
            st.success(f"Found {len(results)} opportunities")
            for job in results:
                st.markdown(f"**[{job['title']}]({job['link']})**  \n"
                            f"🏢 {job['company']} • *{job['source']}*")
                st.markdown("---")
        else:
            st.warning("No opportunities found. Try different keywords or city.")
