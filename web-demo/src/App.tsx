import { useEffect, useState } from 'react';

interface Pattern {
  id: string;
  name: string;
  description: string;
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

function App() {
  const [patterns, setPatterns] = useState<Pattern[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadPatterns = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/patterns`);
        if (!response.ok) {
          throw new Error(`Failed to fetch patterns: ${response.status}`);
        }
        const data = await response.json();
        setPatterns(data.patterns ?? []);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      }
    };

    void loadPatterns();
  }, []);

  return (
    <main style={{ fontFamily: 'Inter, system-ui, sans-serif', padding: '2rem' }}>
      <h1>Nob-Universe Web Demo</h1>
      <p>Explore generated patterns served by the API server.</p>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {patterns.map((pattern) => (
          <li key={pattern.id}>
            <strong>{pattern.name}</strong> — {pattern.description}
          </li>
        ))}
      </ul>
    </main>
  );
}

export default App;
