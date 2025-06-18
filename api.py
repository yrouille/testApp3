from flask import Flask, jsonify, request, abort
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

@app.route('/api/competitors', methods=['GET', 'POST'])
def competitors():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        data = request.get_json(force=True)
        name = data.get('name')
        url = data.get('marketing_url')
        if not name or not url:
            conn.close()
            return jsonify({'error': 'name and marketing_url required'}), 400
        try:
            cur.execute('INSERT INTO competitors (name, marketing_url) VALUES (?, ?)', (name, url))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'competitor exists'}), 400
        conn.close()
        return jsonify({'status': 'ok'}), 201
    else:
        cur.execute('SELECT name, marketing_url FROM competitors')
        rows = cur.fetchall()
        conn.close()
        data = [{'name': r['name'], 'marketing_url': r['marketing_url']} for r in rows]
        return jsonify(data)

@app.route('/api/competitors/<name>', methods=['GET', 'PUT', 'DELETE'])
def competitor_detail(name):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'GET':
        cur.execute('SELECT name, marketing_url FROM competitors WHERE name=?', (name,))
        row = cur.fetchone()
        conn.close()
        if row is None:
            abort(404)
        return jsonify({'name': row['name'], 'marketing_url': row['marketing_url']})
    elif request.method == 'PUT':
        data = request.get_json(force=True)
        url = data.get('marketing_url')
        if not url:
            conn.close()
            return jsonify({'error': 'marketing_url required'}), 400
        cur.execute('UPDATE competitors SET marketing_url=? WHERE name=?', (url, name))
        if cur.rowcount == 0:
            conn.close()
            abort(404)
        conn.commit()
        conn.close()
        return jsonify({'status': 'ok'})
    else:  # DELETE
        cur.execute('DELETE FROM competitors WHERE name=?', (name,))
        if cur.rowcount == 0:
            conn.close()
            abort(404)
        conn.commit()
        conn.close()
        return jsonify({'status': 'deleted'})

if __name__ == '__main__':
    app.run(debug=True)
