# AI Resume Optimizer

This project is an AI-powered Resume Analyzer and Feedback platform. It evaluates resumes against job descriptions, providing an ATS (Applicant Tracking System) score, keyword matches, and feedback for improvement. It runs a local LLM (Ollama with Llama 2) but can be configured to use an API-based online LLM for AWS deployment.

## Features

- ATS score calculation
- Keyword and phrase matching
- Technical, experience, and skills match analysis
- LLM-powered resume critque
- Local LLM support
- Optional API-based LLM integration for AWS deployment


---

## Project Structure
```
resume-optimizer/
│── backend/
│   ├── app/
│   │   ├── models/                # ignore
│   │   ├── routes/                # API endpoints
│   │   │   ├── resume.py          # Resume processing API
│   │   ├── services/              # Resume analysis logic
│   │   │   ├── resume_processing.py
│   │   ├── tests/                 # ignore
│   │   ├── utils/                 # ignore
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
│── temp_resume.pdf                  # Temporary resume storage
│── .venv/ (ignored)                  # Virtual environment
```

---

## Backend Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ZarachxSpace/resume-optimizer.git
cd resume-optimizer
```

### 2. Create a Virtual Environment
```bash
cd resume-optimizer  
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r backend/requirements.txt  # Install backend dependencies
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

## Running the Local LLM (Ollama + Llama 2)

This project uses a local LLM for resume critique. To install and run it:

### 1. Install Ollama
```bash
curl -fsSL https://ollama.ai/install.sh | sh  # For macOS & Linux
```
For Windows, follow Ollama installation guide.

### 2. Pull and Run Llama 2
```
ollama pull llama2
ollama run llama2
```
### 3. API Integration (Ollama Local API)

By default, the backend calls the local LLM at:
```
http://localhost:11434/api/generate
```
**Ensure Ollama is running before making requests.**

## Using an Online LLM API for AWS Deployment

If you plan to deploy the project on AWS and use an online LLM API instead of a local LLM:

1. Update the API URL in `backend/app/routes/resume.py`: 
```
OLLAMA_API_URL = "https://your-online-llm-api.com/v1/generate"
```
2. Ensure authentication credentials are set if required.

3. Comment out local LLM execution in `resume_processing.py`.

---
<!--
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
-->
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

