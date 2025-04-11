"use client"
import { useState } from 'react';
import FileUpload from '../components/FileUpload';
import ResultDisplay from '../components/ResultDisplay';

export default function Home() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [preview, setPreview] = useState('');

  const handleUpload = async (file) => {
    setLoading(true);
    setError('');
    
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await fetch('https://5000-shubham2115-posesdetect-w35er7qzlbk.ws-us118.gitpod.io/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Prediction failed');
      
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-800">
          Pose Detection System
        </h1>
        
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <FileUpload 
            onUpload={handleUpload}
            setPreview={setPreview}
            loading={loading}
          />
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-lg">
              {error}
            </div>
          )}
        </div>

        {(preview || result) && (
          <div className="bg-white rounded-xl shadow-lg p-8">
            {preview && (
              <div className="mb-8">
                <h2 className="text-xl font-semibold mb-4">Preview</h2>
                <img 
                  src={preview} 
                  alt="Preview" 
                  className="max-h-96 rounded-lg object-contain mx-auto"
                />
              </div>
            )}
            
            {result && <ResultDisplay result={result} />}
          </div>
        )}
      </div>
    </div>
  );
}