### APIs repository

from app.core.config import settings
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.extract_skills import extract_top_skills_required, \
    extract_top_skills_of_candidate, calculate_skill_match_score


router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "OK"}


@router.get("/key")
async def get_api_key():
    return {"Key": settings.OPENAI_API_KEY}


@router.post("/extract-the-required-skills")
async def extract_skills(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    skills = extract_top_skills_required(file)
    return {"top_skills_required": skills}


@router.post("/extract-skills-of-candidate")
async def extract_skills_of_candidate(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    skills = extract_top_skills_of_candidate(file)
    return {"top_skills_of_candidate": skills}


@router.post("/match-skill-score")
async def match_score_from_pdfs(
    job_description_file: UploadFile = File(...),
    candidate_resume_file: UploadFile = File(...)
):
    if not (job_description_file.filename.endswith(".pdf") and candidate_resume_file.filename.endswith(".pdf")):
        raise HTTPException(status_code=400, detail="Both files must be PDFs.")

    try:
        # Extract skills from each PDF
        required_skills = extract_top_skills_required(job_description_file)
        candidate_skills = extract_top_skills_of_candidate(candidate_resume_file)

        # Compute the match score
        match_score = calculate_skill_match_score(required_skills, candidate_skills)
        matched_skills = list(set(s.lower() for s in required_skills) & set(s.lower() for s in candidate_skills))

        return {
            "required_skills": required_skills,
            "candidate_skills": candidate_skills,
            "matched_skills": matched_skills,
            "match_score": match_score
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
