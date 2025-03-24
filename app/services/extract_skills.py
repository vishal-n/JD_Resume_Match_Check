### Services containing the core business logic

import os
import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_text_from_pdf(pdf_file):
    with pdfplumber.open(pdf_file.file) as pdf:
        return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())


def extract_top_skills(pdf_file):
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
            # {"role": "system", "content": "You are a helpful assistant skilled in extracting information."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.3,
    )

    skills_text = response.choices[0].message.content.strip()
    skills = [skill.strip() for skill in skills_text.split(",")][:5]
    return skills
