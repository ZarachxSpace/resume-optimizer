import spacy
from spacy.matcher import PhraseMatcher
from rapidfuzz import fuzz
import pdfplumber
import re

nlp = spacy.load("en_core_web_md")


SYNONYMS = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "tf": "tensorflow",
    "pytorch": "torch",
    "js": "javascript",
    "ts": "typescript",
    "gcp": "google cloud",
    "aws": "amazon web services",
    "azure": "microsoft azure",
    "db": "database",
    "sql": "structured query language",
    "nosql": "non relational database",
    "k8s": "kubernetes",
    "docker": "containerization",
    "pipelines": "ci/cd",
    "microservices": "microservice architecture",
    "rest": "restful api",
    "api": "application programming interface",
    "scrum": "agile methodology",
    "pmp": "project management professional",
    "cloud": "cloud computing",
    "devops": "development operations",
    "llm": "large language model",
    "rlhf": "reinforcement learning with human feedback"
}

WEIGHTS = {
    "title": 0.10,
    "tech": 0.25,
    "experience": 0.15,
    "soft_skills": 0.05,
    "phrases": 0.10,
    "ats": 0.15,
    "fuzzy": 0.05,
    "semantic": 0.3,
    "certifications": 0.10,
    "projects": 0.10,
    "extra_curriculars": 0.05,
    "semantic_similarity": 0.10
}

TECH_STACK_MAPPING = {
    "python": {"django", "flask", "fastapi"},
    "machine learning": {"tensorflow", "pytorch", "scikit-learn"},
    "cloud": {"aws", "azure", "gcp"}
}

PHRASES = {
    "machine learning engineer",
    "data scientist",
    "software engineer",
    "backend developer",
    "frontend developer",
    "full stack developer",
    "data analyst",
    "deep learning specialist",
    "natural language processing expert",
    "cloud architect",
    "big data engineer",
    "computer vision developer",
    "ai research scientist"
}

TITLE_KEYWORDS = {
    "software engineer",
    "data scientist",
    "machine learning engineer",
    "backend developer",
    "frontend developer",
    "full stack developer",
    "ai engineer",
    "data analyst",
    "ml researcher",
    "cloud engineer"
}

TECH_KEYWORDS = {
    "python",
    "java",
    "aws",
    "tensorflow",
    "sql",
    "docker",
    "kubernetes",
    "pytorch",
    "react",
    "node.js",
    "c++",
    "javascript",
    "typescript",
    "linux",
    "git",
    "spark",
    "hadoop",
    "graphql",
    "redis",
    "flask",
    "fastapi",
    "postgresql",
    "mongodb"
}

EXPERIENCE_KEYWORDS = {
    "years",
    "experience",
    "bachelor",
    "master",
    "phd",
    "internship",
    "full-time",
    "contract",
    "freelance",
    "consultant",
    "senior",
    "junior",
    "lead",
    "manager"
}

SOFT_SKILLS = {
    "leadership",
    "communication",
    "teamwork",
    "collaboration",
    "problem-solving",
    "critical thinking",
    "creativity",
    "adaptability",
    "time management",
    "mentoring",
    "presentation",
    "negotiation",
    "empathy"
}

CERTIFICATION_KEYWORDS = {
    "aws",
    "azure",
    "gcp",
    "pmp",
    "scrum",
    "cka",
    "ckad",
    "ccna",
    "ocp",
    "google cloud professional",
    "microsoft certified",
    "security+",
    "docker certified associate",
    "deeplearning.ai",
    "machine learning specialization",
    "deep learning specialization",
    
}

PROJECT_KEYWORDS = {
    "developed",
    "implemented",
    "designed",
    "created",
    "automated",
    "optimized",
    "deployed",
    "integrated",
    "scaled",
    "built",
    "migrated",
    "modernized"
}

EXTRA_CURRICULAR_KEYWORDS = {
    "hackathon",
    "volunteer",
    "leader",
    "organizer",
    "speaker",
    "mentor",
    "open source",
    "contributor",
    "club president",
    "community manager"
}

def process_resume(pdf_file, job_description):
    resume_text = extract_text_from_pdf(pdf_file)
    keywords = extract_keywords(resume_text)
    summary = summarize_text(resume_text)
    score = match_job_description(resume_text, job_description)

    # print("DEBUG: match_job_description output BEFORE processing:", score)

    score["overall_fit"] = score.pop("total")

    # print("DEBUG: match_job_description output AFTER renaming:", score)

    return {
        "overall_fit": score["overall_fit"],
        "ats_score": score["ats_score"],
        "tech_match": score["tech_match"],
        "experience_match": score["experience_match"],
        "soft_skills_match": score["soft_skills_match"],
        "certifications_match": score["certifications_match"],
        "projects_match": score["projects_match"],
        "extra_curriculars_match": score["extra_curriculars_match"],
        "semantic_similarity": score["semantic_similarity"],
        "summary": generate_score_explanation(score),
    }


def generate_score_explanation(score):
    explanation = "Your resume has been analyzed based on various aspects relevant to the job description.\n\n"

    explanation += f"🔹 **Overall Fit Score:** {score['overall_fit']}% - This represents how well your resume aligns with the job description.\n"

    explanation += f"✅ **ATS Formatting Score:** {score['ats_score']}% - Indicates how well your resume is structured for Applicant Tracking Systems (ATS).\n"

    explanation += f"💻 **Technical Match:** {score['tech_match']}% - Measures how closely your technical skills align with the job.\n"

    explanation += f"📜 **Experience Match:** {score['experience_match']}% - Evaluates how relevant your past roles are to the job.\n"

    explanation += f"🗣️ **Soft Skills Match:** {score['soft_skills_match']}% - Assesses leadership, communication, and teamwork skills.\n"

    explanation += f"🎓 **Certifications & Training:** {score['certifications_match']}% - Shows how well your certifications align with job requirements.\n"

    explanation += f"🚀 **Projects Match:** {score['projects_match']}% - Examines if you have demonstrated practical applications of skills.\n"

    explanation += f"🌎 **Extracurriculars & Leadership:** {score['extra_curriculars_match']}% - Highlights additional activities that strengthen your profile.\n"

    explanation += f"🤖 **Semantic Similarity Score:** {score['semantic_similarity']}% - AI-powered analysis of how closely your resume’s language matches the JD.\n"

    explanation += "\n💡 Consider improving scores by tailoring your resume to the job description and adding relevant experience!"

    return explanation

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_keywords(text, top_n=10):
    doc = nlp(text.lower())
    keywords = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return list(set(keywords))[:top_n]

def summarize_text(text, max_sentences=3):
    sentences = [sent.text for sent in nlp(text).sents]
    return " ".join(sentences[:max_sentences])

def semantic_similarity(text1, text2):
    doc1 = nlp(text1.lower())
    doc2 = nlp(text2.lower())
    return doc1.similarity(doc2)

def preprocess_text(text):
    doc = nlp(text.lower())
    processed = set()
    for token in doc:
        if not token.is_stop and not token.is_punct:
            lemma = token.lemma_
            processed.add(SYNONYMS.get(lemma, lemma))
    return processed

def match_phrases(text):
    matcher = PhraseMatcher(nlp.vocab)
    patterns = [nlp.make_doc(phrase) for phrase in PHRASES]
    matcher.add("PhraseMatch", patterns)
    doc = nlp(text.lower())
    matches = matcher(doc)
    return len(matches)

def match_category_keywords(text, keywords):
    text_words = preprocess_text(text)
    return len(text_words & keywords) / max(len(keywords), 1)

def fuzzy_match(set1, set2, threshold=80):
    matches = 0
    for word1 in set1:
        for word2 in set2:
            if fuzz.ratio(word1, word2) >= threshold:
                matches += 1
    return matches

def ats_score(resume_text):
    score = 100
    if len(resume_text.split()) > 1000:
        score -= 20
    if resume_text.count("•") < 5:
        score -= 10
    required_sections = ["experience", "education", "skills", "projects"]
    if not all(section in resume_text.lower() for section in required_sections):
        score -= 20
    if "table" in resume_text.lower():
        score -= 10
    if "image" in resume_text.lower():
        score -= 10
    if "comic sans" in resume_text.lower():
        score -= 10
    return max(score, 0)

def match_job_description(resume_text, job_description):
    resume_words = preprocess_text(resume_text)
    job_words = preprocess_text(job_description)

    title_match = len(TITLE_KEYWORDS & resume_words & job_words) / max(len(TITLE_KEYWORDS), 1)
    tech_match = len(TECH_KEYWORDS & resume_words & job_words) / max(len(TECH_KEYWORDS), 1)
    experience_match = len(EXPERIENCE_KEYWORDS & resume_words & job_words) / max(len(EXPERIENCE_KEYWORDS), 1)
    soft_skills_match = len(SOFT_SKILLS & resume_words & job_words) / max(len(SOFT_SKILLS), 1)

    phrase_match_resume = match_phrases(resume_text)
    phrase_match_jd = match_phrases(job_description)
    phrase_score = min((phrase_match_resume + phrase_match_jd) / (2 * len(PHRASES)), 1)

    fuzzy_matches = fuzzy_match(resume_words, job_words)
    fuzzy_score = min(fuzzy_matches / 10, 1)

    certifications_match = match_category_keywords(resume_text, CERTIFICATION_KEYWORDS)
    projects_match = match_category_keywords(resume_text, PROJECT_KEYWORDS)
    extra_curriculars_match = match_category_keywords(resume_text, EXTRA_CURRICULAR_KEYWORDS)

    ats = ats_score(resume_text) / 100

    semantic_score = semantic_similarity(resume_text, job_description)

    total_score = (
        title_match * WEIGHTS["title"] +
        tech_match * WEIGHTS["tech"] +
        experience_match * WEIGHTS["experience"] +
        soft_skills_match * WEIGHTS["soft_skills"] +
        phrase_score * WEIGHTS["phrases"] +
        (ats / 100) * WEIGHTS["ats"] +
        (fuzzy_score / 100) * WEIGHTS["fuzzy"] +
        certifications_match * WEIGHTS["certifications"] +
        projects_match * WEIGHTS["projects"] +
        extra_curriculars_match * WEIGHTS["extra_curriculars"] +
        (semantic_score / 100) * WEIGHTS["semantic"]
    ) * 100

    score_dict = {
        "total": round(total_score, 2),
        "title_match": round(title_match * 100, 2),
        "tech_match": round(tech_match * 100, 2),
        "experience_match": round(experience_match * 100, 2),
        "soft_skills_match": round(soft_skills_match * 100, 2),
        "phrase_match": round(phrase_score * 100, 2),
        "fuzzy_score": round(fuzzy_score * 100, 2),
        "ats_score": round(ats * 100, 2),
        "certifications_match": round(certifications_match * 100, 2),
        "projects_match": round(projects_match * 100, 2),
        "extra_curriculars_match": round(extra_curriculars_match * 100, 2),
        "semantic_similarity": round(semantic_score * 100, 2)
    }

    # print("DEBUG: match_job_description output -->", score_dict)

    return {
        "total": round(total_score, 2),
        "title_match": round(title_match * 100, 2),
        "tech_match": round(tech_match * 100, 2),
        "experience_match": round(experience_match * 100, 2),
        "soft_skills_match": round(soft_skills_match * 100, 2),
        "phrase_match": round(phrase_score * 100, 2),
        "fuzzy_score": round(fuzzy_score * 100, 2),
        "ats_score": round(ats * 100, 2),
        "certifications_match": round(certifications_match * 100, 2),
        "projects_match": round(projects_match * 100, 2),
        "extra_curriculars_match": round(extra_curriculars_match * 100, 2),
        "semantic_similarity": round(semantic_score * 100, 2)
    }


