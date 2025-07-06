import { useEffect, useState } from 'react';
import './App.css';

// For production, use relative paths to work with nginx proxy
const API_BASE = '/api/quotes';

function App() {
  const [quotes, setQuotes] = useState([]);
  const [quote, setQuote] = useState('');
  
  useEffect(() => {
    fetchQuotes();
  }, []);

  const fetchQuotes = () => {
    fetch(API_BASE)
      .then(res => res.json())
      .then(setQuotes)
      .catch(err => console.error('Error fetching quotes:', err));
  };

  const submitQuote = (e) => {
    e.preventDefault();
    if (!quote.trim()) return;
    
    fetch(API_BASE, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ quote })
    })
      .then(res => res.json())
      .then(() => {
        setQuote('');
        fetchQuotes();
      })
      .catch(err => console.error('Error adding quote:', err));
  };

  const deleteQuote = (id) => {
    fetch(`${API_BASE}/${id}`, { method: 'DELETE' })
      .then(() => fetchQuotes())
      .catch(err => console.error('Error deleting quote:', err));
  };

  return (
    <div className="App">
      <h1>QuoteVault</h1>
      <form onSubmit={submitQuote}>
        <input 
          value={quote} 
          onChange={(e) => setQuote(e.target.value)} 
          placeholder="Enter your quote" 
          required
        />
        <button type="submit">Add Quote</button>
      </form>
      <ul>
        {quotes.map(q => (
          <li key={q.id}>
            {q.quote}
            <button onClick={() => deleteQuote(q.id)}>🗑️</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;