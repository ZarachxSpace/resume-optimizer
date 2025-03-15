import { useEffect } from "react";
import "./RoastFeedback.css";

const ResumeFeedback = ({ feedback }) => {
  useEffect(() => {
    console.log("Rendering ResumeFeedback component with:", feedback);
  }, [feedback]);

  if (!feedback || feedback.length === 0) {
    return <p className="no-feedback">No feedback available.</p>;
  }

  return (
    <div className="feedback-container">
      <h2>📋 Resume Feedback Report</h2>
      <ul className="feedback-list">
        {feedback.map((point, index) => (
          <li key={index} className="feedback-item">
            {point}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ResumeFeedback;