import streamlit as st
import requests
import openai
from pypdf import PdfReader
import os

# Set OpenAI API Key
openai.api_key = "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"

# Function to extract job description from a URL
def get_job_description(job_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(job_url, headers=headers)
        
        # Check if the response is successful (status code 200)
        if response.status_code != 200:
            raise Exception(f"Failed to retrieve job posting. Status code: {response.status_code}")
        
        # Print the first 500 characters of the response for debugging purposes
        # This helps ensure that the page content is retrieved as expected
        print(response.text[:500])
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Try to find the job description in the expected HTML structure
        job_description = soup.find("div", class_="jobDescriptionContent")
        
        # If the job description is not found, raise an exception
        if not job_description:
            raise Exception("Job description not found in the HTML content.")
        
        return job_description.text.strip()
    
    except Exception as e:
        print(f"Error: {e}")
        return None
# Function to parse the uploaded resume
def parse_resume(uploaded_resume):
    reader = PdfReader(uploaded_resume)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to interact with ChatGPT for tailoring the resume
def tailor_resume_with_chatgpt(resume_text, job_description):
    prompt = f"""
    Below is the job description for a job posting:
    {job_description}
    
    And here is a candidate's resume:
    {resume_text}
    
    Please tailor the resume by focusing on the relevant skills, experiences, and qualifications that match the job description. 
    Make sure to highlight the most important keywords from the job description and adjust the wording where necessary.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1500
    )
    
    tailored_resume = response['choices'][0]['text'].strip()
    return tailored_resume

# Function to generate a tailored cover letter using ChatGPT
def generate_cover_letter_with_chatgpt(job_description, candidate_name="Candidate"):
    prompt = f"""
    Below is a job description:
    {job_description}
    
    Write a professional cover letter for this job, assuming the candidate is named {candidate_name}. 
    Focus on the candidate's relevant experience, skills, and qualifications that align with the job description. 
    Ensure the letter is formal, concise, and tailored specifically for the job.
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000
    )
    
    cover_letter = response['choices'][0]['text'].strip()
    return cover_letter

# Streamlit UI for uploading resume and job URL input
st.title("Tailored Resume and Cover Letter Generator with ChatGPT")

uploaded_resume = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
job_url = st.text_input("Enter the URL of the job posting")

if st.button("Generate Tailored Resume and Cover Letter"):
    if uploaded_resume and job_url:
        # Parse the resume
        resume_text = parse_resume(uploaded_resume)
        
        # Scrape the job description from the provided URL
        job_description = get_job_description(job_url)
        
        if job_description != "Job description not found.":
            # Tailor the resume with ChatGPT
            tailored_resume = tailor_resume_with_chatgpt(resume_text, job_description)
            
            # Generate a tailored cover letter with ChatGPT
            candidate_name = "Candidate"  # Replace with the actual candidate name if available
            cover_letter = generate_cover_letter_with_chatgpt(job_description, candidate_name)
            
            # Display tailored resume and cover letter
            st.write("### Tailored Resume")
            st.text_area("Your Tailored Resume", tailored_resume, height=300)
            
            st.write("### Tailored Cover Letter")
            st.text_area("Your Tailored Cover Letter", cover_letter, height=200)
        else:
            st.write("Could not retrieve the job description. Please check the URL.")
    else:
        st.write("Please upload your resume and enter a job posting URL.")
