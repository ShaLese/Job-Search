import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from PyPDF2 import PdfReader
import re

# Function to extract job description from a URL
def get_job_description(job_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(job_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Here, we're assuming a generic HTML structure for job descriptions
    job_description = soup.find("div", class_="jobDescriptionContent")
    
    return job_description.text.strip() if job_description else "Job description not found."

# Function to parse the uploaded resume
def parse_resume(uploaded_resume):
    reader = PdfReader(uploaded_resume)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to tailor the resume text based on job description
def tailor_resume(resume_text, job_description):
    # Identify key skills and requirements in the job description
    keywords = re.findall(r'\b\w+\b', job_description.lower())
    keywords = set([word for word in keywords if len(word) > 3])  # Filter short words

    # Highlight relevant skills/keywords from the job description in the resume
    tailored_resume = resume_text
    for keyword in keywords:
        tailored_resume = re.sub(rf"\b({keyword})\b", r"**\1**", tailored_resume, flags=re.IGNORECASE)

    return tailored_resume

# Function to generate a tailored cover letter
def generate_cover_letter(job_description, candidate_name="Candidate"):
    # Simple templated cover letter
    cover_letter = f"""
    Dear Hiring Manager,

    I am excited to apply for this opportunity. With my background in data analysis and a deep understanding of the key skills outlined in the job description, I am confident that I would make a valuable addition to your team.

    In particular, my experience with {job_description[:100]} has prepared me to excel in this role. I am eager to bring my skills in data-driven decision-making and analytical problem-solving to your organization.

    Thank you for considering my application.

    Sincerely,
    {candidate_name}
    """
    return cover_letter

# Streamlit UI for uploading resume and job URL input
st.title("Tailored Resume and Cover Letter Generator")

uploaded_resume = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
job_url = st.text_input("Enter the URL of the job posting")

if st.button("Generate Tailored Resume and Cover Letter"):
    if uploaded_resume and job_url:
        # Parse the resume
        resume_text = parse_resume(uploaded_resume)
        
        # Scrape the job description from the provided URL
        job_description = get_job_description(job_url)
        
        # Tailor the resume based on the job description
        tailored_resume = tailor_resume(resume_text, job_description)
        
        # Generate a tailored cover letter
        candidate_name = "Candidate"  # Replace with the actual candidate name if available
        cover_letter = generate_cover_letter(job_description, candidate_name)
        
        # Display tailored resume and cover letter
        st.write("### Tailored Resume")
        st.text_area("Your Tailored Resume", tailored_resume, height=300)
        
        st.write("### Tailored Cover Letter")
        st.text_area("Your Tailored Cover Letter", cover_letter, height=200)
        
    else:
        st.write("Please upload your resume and enter a job posting URL.")

