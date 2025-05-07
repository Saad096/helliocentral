import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Header from './components/Header';
import DatasetList from './components/DatasetList';

export default function App() {
  const [datasets, setDatasets] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/datasets/')  
      .then(res => setDatasets(res.data.datasets))
      .catch(err => setError('Failed to fetch datasets'));
  }, []);

  return (
    <div className="min-h-screen">
      <Header />
      <main className="p-4">
        {error && <p className="text-red-500">{error}</p>}
        <DatasetList datasets={datasets} />
      </main>
    </div>
  );
}