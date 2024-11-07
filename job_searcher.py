import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import openai

# Function to scrape jobs from Indeed
def scrape_indeed_jobs(job_title, location, salary=None, requirements=None):
    jobs = []
    base_url = f"https://www.indeed.com/jobs?q={job_title}&l={location}"

    # Adding salary filter to the URL if provided
    if salary:
        base_url += f"&salary={salary}"

    # Adding job requirements filter to the URL if provided
    if requirements:
        base_url += f"&q={requirements}"

    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(0, 3):  # Scraping first 3 pages for demonstration
        response = requests.get(base_url + f"&start={page*10}", headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="job_seen_beacon")

        for card in job_cards:
            title = card.find("h2", {"class": "jobTitle"}).text.strip()
            company = card.find("span", {"class": "companyName"}).text.strip()
            salary_text = card.find("span", {"class": "salary-snippet"})
            salary = salary_text.text.strip() if salary_text else "Not disclosed"
            jobs.append({"Title": title, "Company": company, "Salary": salary})
        
        time.sleep(1)  # delay to avoid getting blocked

    return pd.DataFrame(jobs)

# Streamlit UI for user inputs
st.title("Job Scraper")

job_title = st.text_input("Enter job title", "Data Scientist")
location = st.text_input("Enter location", "New York")
salary = st.text_input("Enter desired salary (optional)", "")
requirements = st.text_input("Enter job requirements (optional)", "")

# Add a button to start scraping jobs
if st.button("Search Jobs"):
    if job_title and location:
        # Scrape job data based on user inputs
        df_jobs = scrape_indeed_jobs(job_title, location, salary, requirements)
        if not df_jobs.empty:
            st.write("Scraped Job Data")
            st.dataframe(df_jobs)
        else:
            st.write("No jobs found based on your search criteria.")
    else:
        st.write("Please provide both job title and location.")
