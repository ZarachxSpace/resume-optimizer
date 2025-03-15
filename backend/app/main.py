from fastapi import FastAPI
from backend.app.routes import resume
from backend.database.models import Base, engine
from backend.app.routes import resume
from fastapi.middleware.cors import CORSMiddleware

# Create the FastAPI app instance
app = FastAPI()

# Allow CORS requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow requests from frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include the resume routes
app.include_router(resume.router)

# Health check route
@app.get("/")
def read_root():
    return {"message": "Resume Optimization API is running."}
