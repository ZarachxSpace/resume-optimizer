import React, { useState } from "react";

const ResumeUpload = ({ setResumeFile }) => {
  const [fileName, setFileName] = useState("No file selected");

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    setResumeFile(file);
    setFileName(file ? file.name : "No file selected");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    setResumeFile(file);
    setFileName(file ? file.name : "No file selected");
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  return (
    <div
      className="file-upload-container"
      onDrop={handleDrop}
      onDragOver={handleDragOver}
    >
      <h2>📂 Upload Your Resume</h2>

      <label className="custom-file-upload">
        <input type="file" onChange={handleFileChange} />
        📄 Choose File
      </label>

      <p id="file-name" className="file-name-text">{fileName}</p>
      <p className="drag-drop-text">or drag & drop your file here</p>
    </div>
  );
};

export default ResumeUpload;