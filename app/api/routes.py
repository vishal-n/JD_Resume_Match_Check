### APIs repository

from app.core.config import settings
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.extract_skills import extract_top_skills_required, extract_top_skills_of_candidate

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
