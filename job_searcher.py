import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import openai

# Function to scrape jobs from Indeed
def scrape_indeed_jobs(job_title, location):
    jobs = []
    base_url = f"https://www.indeed.com/jobs?q={job_title}&l={location}"
    headers = {"User-Agent": "Mozilla/5.0"}

    for page in range(0, 3):  # Scraping first 3 pages for demonstration
        response = requests.get(base_url + f"&start={page*10}", headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.find_all("div", class_="job_seen_beacon")

        for card in job_cards:
            title = card.find("h2", {"class": "jobTitle"}).text.strip()
            company = card.find("span", {"class": "companyName"}).text.strip()
            salary = card.find("span", {"class": "salary-snippet"})
            salary = salary.text.strip() if salary else "Not disclosed"
            jobs.append({"Title": title, "Company": company, "Salary": salary})
        
        time.sleep(1)  # delay to avoid getting blocked

    return pd.DataFrame(jobs)

# Streamlit UI for job title and location input
st.title("Job Scraper")
job_title = st.text_input("Enter job title", "Data Scientist")
location = st.text_input("Enter location", "New York")

# Call the scrape function when both inputs are provided
if job_title and location:
    df_jobs = scrape_indeed_jobs(job_title, location)
    st.write("Scraped Job Data")
    st.dataframe(df_jobs)
else:
    st.write("Please provide both job title and location.")
