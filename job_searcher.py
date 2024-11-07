import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Function to scrape jobs from Indeed
def scrape_indeed_jobs(job_title, location, salary=None, requirements=None):
    jobs = []
    base_url = f"https://www.indeed.com/jobs?q={job_title}&l={location}"

    if salary:
        base_url += f"&salary={salary}"
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

# Function to scrape jobs from Glassdoor
def scrape_glassdoor_jobs(job_title, location, salary=None, requirements=None):
    jobs = []
    base_url = f"https://www.glassdoor.com/Job/{location}-{job_title}-jobs-SRCH_KO0,{len(job_title)}_IP1.htm"

    if salary:
        base_url += f"&salary={salary}"
    if requirements:
        base_url += f"&q={requirements}"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("li", class_="react-job-listing")

    for card in job_cards:
        title = card.find("a", {"class": "jobLink"}).text.strip()
        company = card.find("div", {"class": "jobEmpolyerName"}).text.strip()
        salary = card.find("span", {"class": "salaryText"})
        salary = salary.text.strip() if salary else "Not disclosed"
        jobs.append({"Title": title, "Company": company, "Salary": salary})

    return pd.DataFrame(jobs)

# Function to scrape jobs from LinkedIn
def scrape_linkedin_jobs(job_title, location, salary=None, requirements=None):
    jobs = []
    base_url = f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"

    if salary:
        base_url += f"&salary={salary}"
    if requirements:
        base_url += f"&q={requirements}"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("li", class_="result-card")

    for card in job_cards:
        title = card.find("h3", class_="result-card__title").text.strip()
        company = card.find("h4", class_="result-card__subtitle").text.strip()
        salary = "Not disclosed"
        jobs.append({"Title": title, "Company": company, "Salary": salary})

    return pd.DataFrame(jobs)

# Function to scrape jobs from MyJobsInKenya
def scrape_myjobsinkenya_jobs(job_title, location, salary=None, requirements=None):
    jobs = []
    base_url = f"https://www.myjobsinkenya.com/jobs/?keywords={job_title}&location={location}"

    if salary:
        base_url += f"&salary={salary}"
    if requirements:
        base_url += f"&q={requirements}"

    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("div", class_="job-listing")

    for card in job_cards:
        title = card.find("h2", class_="job-title").text.strip()
        company = card.find("span", class_="company-name").text.strip()
        salary = "Not disclosed"  # MyJobsInKenya doesn't list salary explicitly
        jobs.append({"Title": title, "Company": company, "Salary": salary})

    return pd.DataFrame(jobs)

# Mapping of job boards to their respective scraping functions
job_board_scrapers = {
    "Indeed": scrape_indeed_jobs,
    "Glassdoor": scrape_glassdoor_jobs,
    "LinkedIn": scrape_linkedin_jobs,
    "MyJobsInKenya": scrape_myjobsinkenya_jobs
}

# Streamlit UI for user inputs
st.title("Multi-Job Board Scraper")

job_title = st.text_input("Enter job title", "Data Scientist")
location = st.text_input("Enter location", "New York")
salary = st.text_input("Enter desired salary (optional)", "")
requirements = st.text_input("Enter job requirements (optional)", "")

# User can choose which job boards to scrape
selected_boards = st.multiselect(
    "Select job boards to scrape",
    ["Indeed", "Glassdoor", "LinkedIn", "MyJobsInKenya"]
)

# Add a button to start scraping jobs
if st.button("Search Jobs"):
    if job_title and location and selected_boards:
        all_jobs = []
        for board in selected_boards:
            scraper = job_board_scrapers.get(board)
            if scraper:
                st.write(f"Scraping {board}...")
                df_jobs = scraper(job_title, location, salary, requirements)
                if not df_jobs.empty:
                    st.write(f"Jobs from {board}")
                    all_jobs.append(df_jobs)
                else:
                    st.write(f"No jobs found on {board}.")
        if all_jobs:
            combined_jobs = pd.concat(all_jobs, ignore_index=True)
            st.write("Combined Job Data from Selected Boards")
            st.dataframe(combined_jobs)
    else:
        st.write("Please provide both job title, location, and select at least one job board.")
