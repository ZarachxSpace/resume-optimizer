import { useEffect } from "react";
import "./Results.css";

const Results = ({ results }) => {
  useEffect(() => {
    console.log("Rendering Results component with:", results);
  }, [results]);

  if (!results) {
    return <p className="no-results text-visible">No results available.</p>;
  }

  const interpretScore = (score) => {
    if (score >= 80) return "🟢 Excellent Fit";
    if (score >= 60) return "🟡 Moderate Fit";
    return "🔴 Needs Improvement";
  };

  return (
    <div className="results-container">
      <h2 className="text-visible">📊 Resume Analysis Report</h2>

      <div className="score-summary">
        <p className="text-visible"><strong>Overall Fit:</strong> {results?.overall_fit || "N/A"}%</p>
        <p className={`score-status ${results?.overall_fit >= 80 ? "high" : results?.overall_fit >= 60 ? "medium" : "low"} text-visible`}>
          {interpretScore(results?.overall_fit)}
        </p>
      </div>

      <div className="results-grid">
        <div className="result-item text-visible"><strong>ATS Score:</strong> {results?.ats_score || "N/A"}%</div>
        <div className="result-item text-visible"><strong>Technical Match:</strong> {results?.tech_match || "N/A"}%</div>
        <div className="result-item text-visible"><strong>Experience Match:</strong> {results?.experience_match || "N/A"}%</div>
        <div className="result-item text-visible"><strong>Soft Skills Match:</strong> {results?.soft_skills_match || "N/A"}%</div>
        <div className="result-item text-visible"><strong>Certifications Match:</strong> {results?.certifications_match || "N/A"}%</div>
        <div className="result-item text-visible"><strong>Projects Match:</strong> {results?.projects_match || "N/A"}%</div>
        <div className="result-item text-visible"><strong>Extracurricular Match:</strong> {results?.extra_curriculars_match || "N/A"}%</div>
        <div className="result-item text-visible"><strong>Semantic Similarity:</strong> {results?.semantic_similarity || "N/A"}%</div>
      </div>
    </div>
  );
};

export default Results;