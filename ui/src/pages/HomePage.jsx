
import React, { useEffect, useState } from 'react';

const HomePage = () => {
  const [secrets, setSecrets] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchSecrets = async () => {
      const token = localStorage.getItem('token');

      try {
        const response = await fetch('http://localhost:8000/secrets/list', {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch secrets');
        }

        const data = await response.json();
        setSecrets(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchSecrets();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Your Secrets</h1>
      {error && <p className="text-red-500">{error}</p>}
      <ul className="list-disc ml-5">
        {secrets.map((secret, idx) => (
          <li key={idx}>{secret.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default HomePage;
