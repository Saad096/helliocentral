import React from 'react';
import axios from 'axios';

export default function DatasetList({ datasets }) {
  const handleDownload = async (file_id, format) => {
    try {
      const res = await axios.post(
        'http://localhost:8000/datasets/download/',
        { file_id, format },
        { responseType: 'blob' }
      );
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', file_id);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (e) {
      alert('Download failed');
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {datasets.map(ds => (
        <div key={ds.file_id} className="bg-white p-4 rounded-lg shadow-sm">
          <h2 className="font-semibold">{ds.name}</h2>
          <p>Size: {(ds.size / 1024).toFixed(2)} KB</p>
          <button
            className="mt-2 bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
            onClick={() => handleDownload(ds.file_id, ds.format)}
          >
            Download
          </button>
        </div>
      ))}
    </div>
  );
}