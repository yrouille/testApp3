function App() {
  const [newsData, setNewsData] = React.useState({});
  const [marketingData, setMarketingData] = React.useState({});
  const [competitorsList, setCompetitorsList] = React.useState([]);
  const [newName, setNewName] = React.useState('');
  const [newUrl, setNewUrl] = React.useState('');
  const [filter, setFilter] = React.useState('All');

  const API_BASE = 'http://localhost:5000';

  React.useEffect(() => {
    fetch(`${API_BASE}/api/news`).then(r => r.json()).then(setNewsData);
    fetch(`${API_BASE}/api/marketing`).then(r => r.json()).then(setMarketingData);

    const stored = localStorage.getItem('competitors');
    if (stored) {
      setCompetitorsList(JSON.parse(stored));
    } else {
      fetch(`${API_BASE}/api/competitors`) 
        .then(r => r.json())
        .then(data => {
          setCompetitorsList(data);
          localStorage.setItem('competitors', JSON.stringify(data));
        });
    }
  }, []);

  React.useEffect(() => {
    if (Object.keys(marketingData).length) {
      const ctx = document.getElementById('chart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: Object.keys(marketingData),
          datasets: [{
            label: 'Marketing communications',
            data: Object.values(marketingData),
            backgroundColor: 'skyblue'
          }]
        },
        options: {
          responsive: true,
          plugins: { legend: { display: false } }
        }
      });
    }
  }, [marketingData]);

  const competitors = Object.keys(newsData);
  const selectedNews = filter !== 'All' ? (newsData[filter] || []) : [];
  const featureSummaries = selectedNews.map(item => item.summary);

  function addCompetitor(e) {
    e.preventDefault();
    const updated = [...competitorsList, { name: newName, marketing_url: newUrl }];
    setCompetitorsList(updated);
    localStorage.setItem('competitors', JSON.stringify(updated));
    setNewName('');
    setNewUrl('');
  }

  return (
    <div>
      <h1>Competitive Intelligence Dashboard</h1>

      <h2>Competitors</h2>
      <ul>
        {competitorsList.map(c => (
          <li key={c.name}>
            <a href={c.marketing_url} target="_blank">{c.name}</a>
          </li>
        ))}
      </ul>

      <form onSubmit={addCompetitor} style={{ marginBottom: '20px' }}>
        <input value={newName} onChange={e => setNewName(e.target.value)} placeholder="Name" required />
        <input value={newUrl} onChange={e => setNewUrl(e.target.value)} placeholder="Marketing URL" required />
        <button type="submit">Add</button>
      </form>

      <h2>Latest News</h2>
      <select value={filter} onChange={e => setFilter(e.target.value)}>
        <option value="All">All</option>
        {competitors.map(name => <option key={name} value={name}>{name}</option>)}
      </select>

      {(filter === 'All' ? competitors : [filter]).map(name => (
        <div key={name}>
          <h3>{name}</h3>
          {(newsData[name] || []).map((item, i) => (
            <div key={i}>
              <strong>{item.date} - {item.title}</strong>
              <p>{item.summary}</p>
            </div>
          ))}
        </div>
      ))}

      {filter !== 'All' && selectedNews.length > 0 && (
        <div>
          <h4>Summary of highlighted features:</h4>
          <ul>
            {featureSummaries.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
      )}

      <h2>Marketing Communication Activity</h2>
      <canvas id="chart"></canvas>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);
