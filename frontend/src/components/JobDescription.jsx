import React, { useState } from "react";

const JobDescription = ({ setJobDescription }) => {
  const [text, setText] = useState("");

  const handleChange = (e) => {
    setText(e.target.value);
    setJobDescription(e.target.value);
  };

  return (
    <div className="job-description-container">
      <h2 className="text-visible">📝 Enter Job Description</h2>

      <textarea
        className="job-description-textarea"
        placeholder="Paste job description here..."
        value={text}
        onChange={handleChange}
      />

      <p className="word-count text-visible">Word Count: {text.trim().split(/\s+/).length}</p>
    </div>
  );
};

export default JobDescription;