# Services containing the core business logic

import os
import time
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("client: ", client)


def get_chat_completion_with_retry(prompt: str, retries: int = 3,
                                   delay: float = 2.0):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except RateLimitError:
            print(f"Rate limit exceeded. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2
    raise Exception("Exceeded retry attempts due to rate limit.")


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file.file) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages
                       if page.extract_text())


def extract_top_skills_required(pdf_file):
    job_description = extract_text_from_pdf(pdf_file)
    if not job_description:
        raise ValueError("No text extracted from the PDF.")

    prompt = f"""
    Extract the top 5 technical and soft skills from the following job 
    description. Only return the skills as a comma-separated list:
    {job_description}
    """

    skills_text = get_chat_completion_with_retry(prompt)
    skills = [skill.strip() for skill in skills_text.split(",")][:5]
    return skills


def extract_top_skills_of_candidate(pdf_file):
    candidate_skillset = extract_text_from_pdf(pdf_file)
    if not candidate_skillset:
        raise ValueError("No text extracted from the PDF.")
    
    prompt = f"""
    Extract the top 5 technical and soft skills from the following candidate 
    skillset. Only return the skills as a comma-separated list:
    {candidate_skillset}
    """

    skills_text = get_chat_completion_with_retry(prompt)
    candidate_skills = [skill.strip() for skill in skills_text.split(",")][:5]
    return candidate_skills


def calculate_skill_match_score(required_skills: list[str],
                               candidate_skills: list[str]) -> float:
    required_skills_set = set(required_skills)
    candidate_skills_set = set(candidate_skills)

    matched_skills = required_skills_set & candidate_skills_set
    score = (len(matched_skills) / len(required_skills_set)) * 100
    return score if required_skills_set else 0
