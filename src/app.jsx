function App() {
  const [newsData, setNewsData] = React.useState({});
  const [marketingData, setMarketingData] = React.useState({});
  const [filter, setFilter] = React.useState('All');

  React.useEffect(() => {
    fetch('/api/news').then(r => r.json()).then(setNewsData);
    fetch('/api/marketing').then(r => r.json()).then(setMarketingData);
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

  return (
    <div>
      <h1>Competitive Intelligence Dashboard</h1>

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
