// App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [originalImage, setOriginalImage] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = (e) => {
      setOriginalImage(e.target.result);
    };

    reader.readAsDataURL(file);
  };

  const handleImageProcess = async () => {
    // Send originalImage to backend for processing
    const response = await fetch('/process-image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ image: originalImage }),
    });
    const data = await response.json();
    setProcessedImage(data.processedImage);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Transportation Object Detection</h1>
      </header>
      <main>
        <input type="file" onChange={handleImageUpload} />
        <button onClick={handleImageProcess}>Process Image</button>
        {originalImage && (
          <div className="image-container">
            <h2>Original Image</h2>
            <img src={originalImage} alt="Original" />
          </div>
        )}
        {processedImage && (
          <div className="image-container">
            <h2>Processed Image</h2>
            <img src={processedImage} alt="Processed" />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
