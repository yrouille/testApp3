function App() {
  const [newsData, setNewsData] = React.useState({});
  const [marketingData, setMarketingData] = React.useState({});
  const [selected, setSelected] = React.useState('');

  React.useEffect(() => {
    fetch('data/competitor_news.json').then(r => r.json()).then(setNewsData);
    fetch('data/marketing_counts.json').then(r => r.json()).then(setMarketingData);
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
  const selectedNews = selected ? (newsData[selected] || []) : [];
  const featureSummaries = selectedNews.map(item => item.summary);

  return (
    <div>
      <h1>Competitive Intelligence Dashboard</h1>

      <h2>Latest News Across Competitors</h2>
      {competitors.map(name => (
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

      <h2>Latest News for a Specific Competitor</h2>
      <select value={selected} onChange={e => setSelected(e.target.value)}>
        <option value="">-- choose --</option>
        {competitors.map(name => <option key={name} value={name}>{name}</option>)}
      </select>

      {selected && (
        <div>
          <h3>News for {selected}</h3>
          {selectedNews.map((item, i) => (
            <div key={i}>
              <strong>{item.date} - {item.title}</strong>
              <p>{item.summary}</p>
            </div>
          ))}
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
