import json
import sqlite3

def init_db(db_path='data.db'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS competitor_news')
    c.execute('DROP TABLE IF EXISTS marketing_counts')

    c.execute('''CREATE TABLE competitor_news (
                    competitor TEXT,
                    date TEXT,
                    title TEXT,
                    summary TEXT
                )''')
    c.execute('''CREATE TABLE marketing_counts (
                    competitor TEXT PRIMARY KEY,
                    count INTEGER
                )''')

    with open('data/competitor_news.json') as f:
        news_data = json.load(f)
    for comp, items in news_data.items():
        for item in items:
            c.execute(
                'INSERT INTO competitor_news (competitor, date, title, summary) VALUES (?, ?, ?, ?)',
                (comp, item['date'], item['title'], item['summary'])
            )

    with open('data/marketing_counts.json') as f:
        marketing_data = json.load(f)
    for comp, count in marketing_data.items():
        c.execute(
            'INSERT INTO marketing_counts (competitor, count) VALUES (?, ?)',
            (comp, count)
        )

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print('Database initialized')
