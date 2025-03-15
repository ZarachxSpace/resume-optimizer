# AI Resume Optimizer

This project evaluates resumes against job descriptions using AI, providing ATS-based scores, keyword matching, and structured feedback.

## Features

- Resume Analysis – Matches resumes with job descriptions based on ATS, technical skills, experience, and semantic similarity.
- Keyword Matching – Identifies missing keywords relevant to the job description.
- Structured Feedback – Provides specific suggestions for improving the resume.
- Simple Interface – Upload a resume, enter a job description, and get real-time analysis.

---

## Project Structure
```
resume-optimizer/
│── backend/
│   ├── app/
│   │   ├── models/                # Database models
│   │   ├── routes/                # API endpoints
│   │   │   ├── resume.py          # Resume processing API
│   │   ├── services/              # Resume analysis logic
│   │   │   ├── resume_processing.py
│   │   ├── tests/                 # Unit tests
│   │   ├── utils/                 # Utility functions
│   │   └── main.py                # FastAPI entry point
│   ├── database/                  # Database migrations
│   ├── requirements.txt           # Python dependencies
│
│── frontend/
│   ├── src/
│   │   ├── components/            # React components
│   │   ├── assets/                # Static files
│   │   ├── App.jsx                # Main React entry
│   │   └── index.jsx              # React root
│   ├── public/                    # Static public files
│   ├── package.json               # Frontend dependencies
│
│── .gitignore                      # Ignored files
│── README.md                        # Documentation
│── alembic.ini                      # Alembic migrations config
│── temp_resume.pdf (ignored)         # Temporary resume storage
│── .venv/ (ignored)                  # Virtual environment
```

---

## Backend Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/resume-optimizer.git
cd resume-optimizer
```

### 2. Create a Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Configure PostgreSQL
1. Ensure **PostgreSQL is running**.
2. Create a new database:
   ```sql
   CREATE DATABASE resume_optimizer;
   ```
3. Update `DATABASE_URL` in `backend/app/config.py`:
   ```python
   DATABASE_URL = "postgresql://USERNAME:PASSWORD@localhost:5432/resume_optimizer"
   ```

### 5. Run Database Migrations
```bash
alembic upgrade head
```

### 6. Start the Backend Server
```bash
uvicorn backend.app.main:app --reload
```
API documentation is available at:  
`http://127.0.0.1:8000/docs`

---

## Frontend Setup

### 1. Navigate to the Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start the Frontend Server
```bash
npm run dev
```
The application should now be running at:  
`http://localhost:5173`

---

## Running the Project on a New System

If running this on a new system:
1. Clone the repository.
2. Install backend and frontend dependencies.
3. Set up PostgreSQL and apply migrations.
4. Start the backend and frontend servers.

---

## Deployment to AWS

### 1. Deploy Backend to AWS EC2
1. SSH into your **AWS EC2 instance**:
   ```bash
   ssh ubuntu@your-aws-instance-ip
   ```
2. Install **PostgreSQL**:
   ```bash
   sudo apt update && sudo apt install postgresql -y
   ```
3. Pull the backend from GitHub:
   ```bash
   git clone https://github.com/YOUR_USERNAME/resume-optimizer.git
   cd resume-optimizer/backend
   ```
4. Set up environment variables (`.env`):
   ```bash
   touch .env
   ```
   Add:
   ```
   DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/resume_optimizer
   ```
5. Run database migrations:
   ```bash
   alembic upgrade head
   ```
6. Start the backend server:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
   ```
7. Verify the API is running:
   ```bash
   curl http://your-aws-instance-ip:8000/docs
   ```

### 2. Deploy Frontend to AWS S3 & CloudFront
1. Inside `frontend/`:
   ```bash
   npm run build
   ```
2. Upload `dist/` to AWS S3 bucket:
   ```bash
   aws s3 cp --recursive dist/ s3://your-bucket-name
   ```
3. Configure **CloudFront** for a public URL.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|---------|------------|
| POST | `/resume/analyze` | Uploads resume & analyzes against job description |
| POST | `/resume/feedback` | Generates resume improvement feedback |
| GET | `/resume/matches/{resume_id}` | Fetches job match scores |

---

## To-Do List & Future Improvements
- Improve Scoring Algorithm
- Enhance Resume Feedback
- Deploy to AWS Lambda
- Build a Mobile-Friendly UI
- Support Multiple Resume Formats (DOCX, TXT)

---

## License
MIT License - Free to use & contribute.  
Feel free to fork and improve the project.

---

## Contributors
**Zarach** – [GitHub Profile](https://github.com/ZarachxSpace)

---

## Support
For any issues, open a GitHub **issue** or contact via **email**.

