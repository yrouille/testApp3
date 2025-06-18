from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/news')
def all_news():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT competitor, date, title, summary FROM competitor_news')
    rows = cur.fetchall()
    conn.close()
    data = {}
    for row in rows:
        data.setdefault(row['competitor'], []).append({
            'date': row['date'],
            'title': row['title'],
            'summary': row['summary']
        })
    return jsonify(data)

@app.route('/api/news/<competitor>')
def news_for_competitor(competitor):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT date, title, summary FROM competitor_news WHERE competitor=?', (competitor,))
    rows = cur.fetchall()
    conn.close()
    data = [{
        'date': row['date'],
        'title': row['title'],
        'summary': row['summary']
    } for row in rows]
    return jsonify(data)

@app.route('/api/marketing')
def marketing_counts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT competitor, count FROM marketing_counts')
    rows = cur.fetchall()
    conn.close()
    data = {row['competitor']: row['count'] for row in rows}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
