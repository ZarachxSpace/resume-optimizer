from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

Base = declarative_base()

# PostgreSQL Connection URL
DATABASE_URL = "postgresql://resume_user:resume_password@localhost:5432/resume_optimizer"

# Create database engine
engine = create_engine(DATABASE_URL)

# Create Session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)  # Ensure this exists
    phone = Column(String, nullable=True)  # Ensure this exists
    extracted_text = Column(Text, nullable=False)


# New DB variables
class JobMatch(Base):
    __tablename__ = "job_matches"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_description = Column(Text, nullable=False)
    match_score = Column(Float, nullable=True)  # <-- Ensure this exists
    ats_score = Column(Float, nullable=True)  # <-- Ensure this exists
    tech_match = Column(Float, nullable=True)  # 🔹 Rename technical_match → tech_match
    experience_match = Column(Float, nullable=True)  # <-- Ensure this exists
    soft_skills_match = Column(Float, nullable=True)  # <-- Ensure this exists
    certifications_match = Column(Float, nullable=True)  # <-- Ensure this exists
    projects_match = Column(Float, nullable=True)  # <-- Ensure this exists
    extra_curriculars_match = Column(Float, nullable=True)  # <-- Ensure this exists
    semantic_similarity = Column(Float, nullable=True)  # <-- Ensure this exists

def init_db():
    """Create database tables if they don't exist"""
    Base.metadata.create_all(bind=engine)