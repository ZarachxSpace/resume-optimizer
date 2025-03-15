import React, { useState } from "react";
import JobDescription from "./components/JobDescription.jsx";
import ResumeUpload from "./components/ResumeUpload.jsx";
import Results from "./components/Results.jsx";
import RoastFeedback from "./components/RoastFeedback.jsx";
import "./App.css";

function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState(null);
  const [matchData, setMatchData] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyzeResume = async () => {
    if (!resumeFile || !jobDescription) {
      alert("Please upload a resume and enter a job description.");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("file", resumeFile);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch("http://localhost:8000/resume/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      console.log("Received Analysis Data:", data);
      setMatchData(data);
    } catch (error) {
      console.error("Error analyzing resume:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGetFeedback = async () => {
    if (!resumeFile || !jobDescription) {
        alert("Please upload a resume and enter a job description.");
        return;
    }
    setLoading(true);
    const formData = new FormData();
    formData.append("file", resumeFile);
    formData.append("job_description", jobDescription);

    try {
        const response = await fetch("http://localhost:8000/resume/roast", {
            method: "POST",
            body: formData,
        });

        console.log("Full Response Object:", response);
        console.log("Response Status:", response.status);

        const data = await response.json();
        console.log("Received Roast Feedback:", data);

        // Ensure the roast data exists before setting it
        if (data && data.roast) {
            setFeedback(data.roast);
        } else {
            console.warn("Roast feedback is missing in response:", data);
            setFeedback("⚠️ No feedback available. Please try again.");
        }
    } catch (error) {
        console.error("Error fetching resume feedback:", error);
        setFeedback("❌ Error fetching feedback. Please try again.");
    } finally {
        setLoading(false);
    }
};

  return (
    <div className="container">
      <h1>AI Resume Optimizer</h1>

      {/* Explanation Box */}
      <div className="explanation">
        <p>
          This AI-powered tool analyzes your resume against job descriptions and provides an
          ATS-based score, keyword matching, and personalized feedback to improve your chances of getting hired.
        </p>
      </div>

      <JobDescription setJobDescription={setJobDescription} />
      <ResumeUpload setResumeFile={setResumeFile} />
      {loading && <p>Processing... Please wait.</p>}

      <button onClick={handleAnalyzeResume} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>

      <button onClick={handleGetFeedback} disabled={loading}>
        {loading ? "Fetching Feedback..." : "Get Resume Feedback"}
      </button>

      {/* Display results only when data is available */}
      {matchData && <Results results={matchData} />}
      {feedback && <RoastFeedback feedback={feedback} />}

      <div className="footer">© 2025 Zarach</div>
    </div>
  );
}

export default App;