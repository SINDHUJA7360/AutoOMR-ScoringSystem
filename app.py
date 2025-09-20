from flask import Flask, request, jsonify
import cv2
import numpy as np
import sqlite3
import json
from omr_engine import process_omr_sheet

app = Flask(__name__)

# This is the correct Answer Key from our previous steps.
ANSWER_KEY = {
    0: 0, 1: 2, 2: 1, 3: 3, 4: 0, 5: 2, 6: 0, 7: 2, 8: 1, 9: 2, 10: 1, 11: 3, 12: 1, 13: 1, 14: 2, 15: 1, 16: 0, 17: 1, 18: 3, 19: 0, 20: 3, 21: 1, 22: 3, 23: 2, 24: 3, 25: 0, 26: 2, 27: 0, 28: 3, 29: 3, 30: 0, 31: 3, 32: 2, 33: 2, 34: 0, 35: 3, 36: 2, 37: 0, 38: 2, 39: 0, 40: 2, 41: 3, 42: 1, 43: 0, 44: 2, 45: 0, 46: 1, 47: 3, 48: 1, 49: 3, 50: 0, 51: 2, 52: 1, 53: 0, 54: 2, 55: 1, 56: 0, 57: 2, 58: 1, 59: 3, 60: 0, 61: 2, 62: 1, 63: 0, 64: 2, 65: 1, 66: 0, 67: 2, 68: 1, 69: 3, 70: 0, 71: 2, 72: 1, 73: 0, 74: 2, 75: 1, 76: 0, 77: 2, 78: 1, 79: 3, 80: 0, 81: 2, 82: 1, 83: 0, 84: 2, 85: 1, 86: 0, 87: 2, 88: 1, 89: 3, 90: 0, 91: 2, 92: 1, 93: 0, 94: 2, 95: 1, 96: 0, 97: 2, 98: 1, 99: 3
}

DATABASE = 'results.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn

def create_table():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            total_score INTEGER NOT NULL,
            subject_scores TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/api/evaluate_omr', methods=['POST'])
def evaluate_omr():
    if 'omr_sheet' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['omr_sheet']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    image_bytes = file.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = process_omr_sheet(image, ANSWER_KEY)
    
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO results (filename, total_score, subject_scores) VALUES (?, ?, ?)",
            (file.filename, results['total_score'], json.dumps(results['subject_scores']))
        )
        conn.commit()
    except Exception as e:
        return jsonify({"error": f"Database insertion failed: {e}"}), 500
    finally:
        conn.close()

    return jsonify({"message": "Evaluation successful", "results": results})

if __name__ == '__main__':
    app.run(debug=True)