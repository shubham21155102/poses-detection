const ResultDisplay = ({ result }) => {
  const poseDescriptions = {
    sitting: "The person is in a seated position",
    standing: "The person is standing upright",
    balancing: "The person is maintaining balance",
    falling: "The person is in a falling motion",
    hugging: "The person is hugging someone",
    lookingup: "The person is looking upwards",
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-4">Detection Results</h2>
      
      <div className="bg-blue-50 p-6 rounded-lg">
        <div className="flex items-center gap-4">
          <span className="text-4xl">🎯</span>
          <div>
            <h3 className="text-xl font-semibold text-gray-800">
              {result.predicted_class}
              <span className="ml-2 text-blue-600">
                ({Math.round(result.confidence * 100)}% confidence)
              </span>
            </h3>
            <p className="text-gray-600 mt-1">
              {poseDescriptions[result.predicted_class.toLowerCase()]}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="p-4 bg-gray-50 rounded-lg">
          <p className="text-sm font-medium text-gray-500">Possible Multi-Poses</p>
          <p className="mt-1 text-gray-700">
            Our system is currently learning to detect multiple poses simultaneously.
            Stay tuned for updates!
          </p>
        </div>
        
        <div className="p-4 bg-gray-50 rounded-lg">
          <p className="text-sm font-medium text-gray-500">Analysis Details</p>
          <ul className="mt-1 space-y-1 text-gray-700">
            <li>Input Resolution: 48x48px</li>
            <li>Model Type: Deep Learning CNN</li>
            <li>Processing Time: &lt;1s</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;