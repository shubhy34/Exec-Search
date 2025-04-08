import streamlit as st
import requests
from serpapi import GoogleSearch
import re

st.set_page_config(page_title="Executive LinkedIn Finder")
st.title("🔍 Executive LinkedIn Profile Finder")

SERPAPI_KEY = "0a72b64bccab9ced37cbd5c071e9368b829facd6f6e0a7d42d3e89bf8c2f0d55"

@st.cache_data(ttl=3600)
def google_search(query, num=5):
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": num
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        return results.get("organic_results", [])
    except Exception as e:
        st.error(f"Search error: {e}")
        return []

def extract_linkedin_url(results):
    for res in results:
        link = res.get("link", "")
        if "linkedin.com/in/" in link:
            return link
    return None

def fetch_linkedin_profile_summary(linkedin_url):
    # Placeholder - actual scraping of LinkedIn requires LinkedIn API or proxy/browser automation
    return {
        "current_company": "[Sample Company]",
        "start_date": "[Start Date]"
    }

# Streamlit input UI
with st.form("exec_form"):
    exec_name = st.text_input("Executive Full Name", placeholder="e.g. Manish Singh")
    company_name = st.text_input("Company Name", placeholder="e.g. Microsoft")
    job_title = st.text_input("Job Title", placeholder="e.g. Senior Software Engineer")
    submitted = st.form_submit_button("Search LinkedIn Profile")

if submitted:
    if not exec_name or not company_name or not job_title:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("Searching Google for LinkedIn profiles..."):
            query = f"{exec_name} {company_name} {job_title} site:linkedin.com/in"
            search_results = google_search(query)
            linkedin_url = extract_linkedin_url(search_results)

        if linkedin_url:
            st.success("LinkedIn profile found!")
            st.markdown(f"🔗 [View LinkedIn Profile]({linkedin_url})")
            # Simulated scraping
            profile_data = fetch_linkedin_profile_summary(linkedin_url)
            st.write("**Current Company:**", profile_data['current_company'])
            st.write("**Start Date:**", profile_data['start_date'])
        else:
            st.error("LinkedIn profile not found. You can try checking other sources or rephrasing the input.")
