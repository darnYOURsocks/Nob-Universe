import React, { useEffect, useState } from 'react';

type Pattern = {
  id: number;
  name: string;
  description: string;
};

function App() {
  const [patterns, setPatterns] = useState<Pattern[]>([]);
  const [status, setStatus] = useState('loading...');

  useEffect(() => {
    fetch('/api/patterns')
      .then((res) => res.json())
      .then((data) => {
        setPatterns(data.patterns || []);
        setStatus(data.status || 'unknown');
      })
      .catch(() => setStatus('unavailable'));
  }, []);

  return (
    <main style={{ fontFamily: 'sans-serif', padding: '2rem' }}>
      <h1>NOB Universe Demo</h1>
      <p>API status: {status}</p>
      <ul>
        {patterns.map((pattern) => (
          <li key={pattern.id}>
            <strong>{pattern.name}</strong>: {pattern.description}
          </li>
        ))}
      </ul>
    </main>
  );
}

export default App;
