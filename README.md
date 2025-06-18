# Competitive Intelligence Dashboard

This project provides a lightweight dashboard for monitoring the latest news and marketing activity of solutions competing with Fredhopper and XO.

The interface is now built in **React** and uses local JSON files located in the `data/` directory. You can update those files with your own observations or integrate a scraper.

## Getting Started

1. Install Node dependencies (used here only for optional future extensions):
   ```bash
   npm install
   ```

2. Serve the static site. One simple way is using Python's built‑in server:
   ```bash
   python3 -m http.server 8000
   ```
   Then open `http://localhost:8000/index.html` in your browser.

The dashboard exposes three key features:

1. **Latest News Across Competitors** – a list of updates for each solution.
2. **Latest News for a Specific Competitor** – choose a competitor from the drop‑down to see its news and a summary of the highlighted features.
3. **Marketing Communication Activity** – a bar chart comparing how frequently each solution communicates in marketing channels.

Feel free to modify or replace the `data/*.json` files to tailor the dashboard to your own research.

### Legacy Streamlit option
You can still run the original Streamlit interface with:
```bash
streamlit run app.py --server.headless true
```
This may report a blocked IP check but otherwise serves the same data.
