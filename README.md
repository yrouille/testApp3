# Competitive Intelligence Dashboard

This project provides a lightweight dashboard for monitoring the latest news and marketing activity of solutions competing with Fredhopper and XO.

The interface is built in **React** and now relies on a small Flask API that
serves data from an SQLite database. Sample JSON files in the `data/` directory
can be imported into the database so the dashboard updates dynamically.

## Getting Started

1. Install Python requirements and optional Node dependencies:
   ```bash
   pip install -r requirements.txt
   npm install
   ```

2. Initialize the SQLite database and start the API server:
   ```bash
   python db_setup.py       # populate data.db from JSON files
   python api.py            # start Flask on http://localhost:5000
   ```

3. Serve the static site. One simple way is using Python's built‑in server:
   ```bash
   python3 -m http.server 8000
   ```
   Then open `http://localhost:8000/index.html` in your browser.
   The page expects the API to be reachable at `http://localhost:5000`.

The dashboard exposes two key features:

1. **Latest News** – view updates across all competitors or filter the list to a single solution. When a competitor is selected, a summary of the highlighted features is shown.
2. **Marketing Communication Activity** – a bar chart comparing how frequently each solution communicates in marketing channels.

Feel free to modify or replace the `data/*.json` files to tailor the dashboard to your own research.

### Legacy Streamlit option
You can still run the original Streamlit interface with:
```bash
streamlit run app.py --server.headless true
```
This may report a blocked IP check but otherwise serves the same data.
