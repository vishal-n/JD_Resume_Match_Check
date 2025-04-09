### Services containing the core business logic

import os
import pdfplumber
from typing import List
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file.file) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())


def extract_top_skills_required(pdf_file):
    job_description = extract_text_from_pdf(pdf_file)
    if not job_description:
        raise ValueError("No text extracted from the PDF.")

    prompt = f"""
    Extract the top 5 technical and soft skills from the following job description.
    Only return the skills as a comma-separated list:
    {job_description}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.3,
    )

    skills_text = response.choices[0].message.content.strip()
    skills = [skill.strip() for skill in skills_text.split(",")][:5]
    return skills


def extract_top_skills_of_candidate(pdf_file):
    candidate_skillset = extract_text_from_pdf(pdf_file)
    if not candidate_skillset:
        raise ValueError("No text extracted from the PDF.")
    
    prompt = f"""
    Extract the top 5 technical and soft skills from the following candidate skillset.
    Only return the skills as a comma-separated list:
    {candidate_skillset}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.3,
    )

    top_five_skills_of_candidate = response.choices[0].message.content.strip()
    candidate_skills = [skill.strip() for skill in top_five_skills_of_candidate.split(",")][:5]
    return candidate_skills


def calculate_skill_match_score(required_skills: list[str], candidate_skills: list[str]) -> float:
    required_skills_set = set(required_skills)
    candidate_skills_set = set(candidate_skills)

    # intersection = required_skills_set.intersection(candidate_skills_set)
    # match_percentage = len(intersection) / len(required_skills_set) * 100
    # return match_percentage

    matched_skills = required_skills_set & candidate_skills_set
    score = (len(matched_skills) / len(required_skills_set)) * 100 if required_skills_set else 0
    return score 
