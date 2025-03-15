import requests
from fastapi import APIRouter, UploadFile, File, Form, Depends, Query
from sqlalchemy.orm import Session
from backend.database.models import SessionLocal, Resume, JobMatch
from backend.app.services.resume_processing import process_resume, extract_text_from_pdf, generate_score_explanation
from typing import Optional, List

router = APIRouter(prefix="/resume", tags=["Resume Processing"])
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama2"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.post("/analyze")
# async def analyze_resume(
#         file: UploadFile = File(...),
#         job_description: str = Form(...),
#         db: Session = Depends(get_db)
# ):
#     contents = await file.read()
#     with open("temp_resume.pdf", "wb") as f:
#         f.write(contents)
#
#     result = process_resume("temp_resume.pdf", job_description)
#
#     new_resume = Resume(name=file.filename, extracted_text=result["text"])
#     db.add(new_resume)
#     db.commit()
#     db.refresh(new_resume)
#
#     new_match = JobMatch(
#         resume_id=new_resume.id,
#         job_description=job_description,
#         match_score=result["score"]["total"],
#         title_match=result["score"]["title_match"],
#         tech_match=result["score"]["tech_match"],
#         experience_match=result["score"]["experience_match"],
#         soft_skill_match=result["score"]["soft_skill_match"]
#     )
#     db.add(new_match)
#     db.commit()
#
#     return result

@router.post("/analyze")
async def analyze_resume(
        file: UploadFile = File(...),
        job_description: str = Form(...),
        db: Session = Depends(get_db)
):
    contents = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)

    result = process_resume("temp_resume.pdf", job_description)

    print("DEBUG: process_resume() output -->", result)  # Debugging print

    if "overall_fit" not in result:
        return {"error": "Missing key 'overall_fit' in resume analysis result"}

    new_resume = Resume(name=file.filename, extracted_text=result["summary"])
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    new_match = JobMatch(
        resume_id=new_resume.id,
        job_description=job_description,
        match_score=result["overall_fit"],
        ats_score=result["ats_score"],
        tech_match=result["tech_match"],
        experience_match=result["experience_match"],
        soft_skills_match=result["soft_skills_match"],
        certifications_match=result["certifications_match"],
        projects_match=result["projects_match"],
        extra_curriculars_match=result["extra_curriculars_match"],
        semantic_similarity=result["semantic_similarity"]
    )
    db.add(new_match)
    db.commit()

    return {
        **result,  # Return the full result
        "summary": generate_score_explanation(result)  # Add Explanation
    }


@router.get("/matches/{resume_id}")
def get_matches(
        resume_id: int,
        limit: int = Query(10, ge=1),  # Pagination Limit results
        offset: int = Query(0, ge=0),  # Pagination Offset
        min_score: Optional[float] = Query(0.0, ge=0.0),  # Filter Minimum match score
        min_tech_match: Optional[float] = Query(0.0, ge=0.0),  # Filter Minimum tech match
        min_ats_score: Optional[float] = Query(0.0, ge=0.0),  # Filter Minimum ATS score
        min_experience_match: Optional[float] = Query(0.0, ge=0.0),  # Filter Minimum experience match
        job_keyword: Optional[str] = Query(None),  # Filter Job description keyword
        db: Session = Depends(get_db)
):
    query = db.query(JobMatch).filter(JobMatch.resume_id == resume_id)

    if min_score:
        query = query.filter(JobMatch.match_score >= min_score)
    if min_tech_match:
        query = query.filter(JobMatch.tech_match >= min_tech_match)
    if min_ats_score:
        query = query.filter(JobMatch.ats_score >= min_ats_score)
    if min_experience_match:
        query = query.filter(JobMatch.experience_match >= min_experience_match)
    if job_keyword:
        query = query.filter(JobMatch.job_description.ilike(f"%{job_keyword}%"))

    matches = query.offset(offset).limit(limit).all()

    if not matches:
        return {"message": "No matches found for this resume."}

    return [
        {
            "match_id": match.id,
            "job_description": match.job_description,
            "match_score": match.match_score,
            "technical_match": match.tech_match,
            "experience_match": match.experience_match,
            "ats_score": match.ats_score,
            "soft_skills_match": match.soft_skills_match,
            "certifications_match": match.certifications_match,
            "projects_match": match.projects_match,
            "extra_curriculars_match": match.extra_curriculars_match,
            "semantic_similarity": match.semantic_similarity
        }
        for match in matches
    ]

# def generate_roast(resume_text, job_description):
#     prompt = (
#         "You are a professional technical recruiter evaluating resumes for highly competitive roles in the tech industry. "
#         "Your task is to carefully analyze the following resume in relation to a specific job description and provide an objective, detailed critique.\n\n"
#
#         "### Step 1: Identify Resume Weaknesses\n"
#         "Compare the resume against the job description and list **specific weaknesses**, including:\n"
#         "- Missing or underdeveloped skills that are crucial for the role.\n"
#         "- Experience gaps or lack of demonstrated impact in key areas.\n"
#         "- Weak or vague descriptions that do not align with the job's expectations.\n"
#         "- Irrelevant sections or content that do not contribute to the job application.\n"
#         "- Formatting or clarity issues that could make it harder for recruiters to assess suitability.\n\n"
#
#         "### Step 2: Provide an Actionable Improvement Plan\n"
#         "For each weakness, suggest **specific ways to strengthen the resume**, including:\n"
#         "- How to restructure or rewrite sections for better alignment with the job.\n"
#         "- What measurable achievements or quantifiable impact to add.\n"
#         "- Suggested projects that would demonstrate relevant skills.\n"
#         "- Certifications that could enhance credibility for this role.\n"
#         "- Experience-building opportunities such as internships, open-source contributions, or relevant hands-on work.\n\n"
#
#         "### Important Guidelines\n"
#         "- **Only base your feedback on the provided resume and job description.** Avoid assumptions.\n"
#         "- **Be direct and highly specific.** Do not provide generic feedback.\n"
#         "- **Ensure all suggestions directly align with the job description's requirements.**\n"
#         "- **Do not recommend unnecessary soft skills or personal statements unless directly relevant.**\n\n"
#
#         "### Resume Text:\n{resume_text}\n\n"
#         "### Job Description:\n{job_description}\n"
#     ).format(resume_text=resume_text, job_description=job_description)
#
#     payload = {
#         "model": OLLAMA_MODEL,
#         "prompt": prompt,
#         "stream": False
#     }
#
#     response = requests.post(OLLAMA_API_URL, json=payload)
#     response.raise_for_status()
#     return response.json().get("response", "No response from LLM.")

def generate_roast(resume_text, job_description):
    prompt = (
        "You are an experienced recruiter evaluating resumes for a competitive tech role. "
        "Your job is to analyze the resume and **speak directly to the candidate**, highlighting weaknesses "
        "and providing specific, actionable steps to improve their resume.\n\n"
        
        "### **Instructions:**\n"
        "1️⃣ Identify **specific weaknesses** where the resume does not align with the job.\n"
        "2️⃣ Highlight missing skills, unclear achievements, or formatting issues.\n"
        "3️⃣ Provide **direct, constructive feedback in second-person** (e.g., 'You need to...').\n"
        "4️⃣ Avoid speaking in third person (e.g., 'The candidate should...')\n"
        "5️⃣ Format the response using structured bullet points, **keeping each point concise**.\n\n"

        "### **Your Feedback Should Include:**\n"
        "📌 **What’s missing?** (Skills, experience, structure) \n"
        "🛠️ **How to improve?** (Specific, actionable steps) \n"
        "✅ **What changes should be made?** (Formatting, wording, technical depth)\n\n"
        
        "**Your response should follow this format:**\n"
        "- 🔹 *[Highlight issue]* - *[How to improve it]*\n\n"

        "**Example:**\n"
        "- 🔹 *Your resume lacks measurable achievements.* - *Instead of saying 'Developed models,' say 'Developed ML models that improved accuracy by 20%'.*\n"
        "- 🔹 *Your job experience section is too vague.* - *You need to quantify impact using metrics like 'Reduced latency by 30%' or 'Automated processes saving 10 hours per week'.*\n\n"

        "**Now, analyze the following resume and provide direct feedback:**\n\n"
        
        "### **Resume Text:**\n{resume_text}\n\n"
        "### **Job Description:**\n{job_description}\n"
    ).format(resume_text=resume_text, job_description=job_description)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, json=payload)
    response.raise_for_status()

    raw_response = response.json().get("response", "No response from LLM.")

    # Convert response to bullet points
    feedback_points = list(filter(None, raw_response.split("\n")))

    return feedback_points


# @router.post("/roast")
# async def roast_resume(
#     file: UploadFile = File(...),
#     job_description: str = Form(...)
# ):
#     contents = await file.read()
#     with open("temp_resume.pdf", "wb") as f:
#         f.write(contents)
#
#     resume_text = extract_text_from_pdf("temp_resume.pdf")
#
#     if not resume_text.strip():
#         return {"error": "Failed to extract text from the uploaded resume."}
#
#     roast_feedback = generate_roast(resume_text, job_description)
#     return {"roast": roast_feedback}

@router.post("/roast")
async def roast_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    contents = await file.read()
    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)

    resume_text = extract_text_from_pdf("temp_resume.pdf")

    if not resume_text.strip():
        return {"error": "Failed to extract text from the uploaded resume."}

    roast_feedback = generate_roast(resume_text, job_description)
    return {"roast": roast_feedback}