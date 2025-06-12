from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = './database/planner.db'

# DB 초기화
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, title TEXT, deadline TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS plans (id INTEGER PRIMARY KEY, date TEXT, subject TEXT, content TEXT, expected_time INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, subject TEXT, duration INTEGER, date TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT, subject TEXT, date TEXT)''')
conn.commit()
conn.close()

@app.route('/api/goals', methods=['GET', 'POST'])
def handle_goals():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if request.method == 'POST':
        data = request.get_json()
        c.execute("INSERT INTO goals (title, deadline) VALUES (?, ?)", (data['title'], data['deadline']))
        conn.commit()
        return jsonify({'status': 'Goal added'}), 201
    else:
        c.execute("SELECT * FROM goals")
        rows = c.fetchall()
        return jsonify(rows)

@app.route('/api/plans', methods=['POST'])
def add_plan():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO plans (date, subject, content, expected_time) VALUES (?, ?, ?, ?)",
              (data['date'], data['subject'], data['content'], data['expected_time']))
    conn.commit()
    return jsonify({'status': 'Plan added'})

@app.route('/api/records', methods=['POST'])
def add_record():
    data = request.get_json()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO records (subject, duration, date) VALUES (?, ?, ?)",
              (data['subject'], data['duration'], data['date']))
    conn.commit()
    return jsonify({'status': 'Record added'})

@app.route('/api/report', methods=['GET'])
def report():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT subject, SUM(duration) FROM records GROUP BY subject")
    rows = c.fetchall()
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
