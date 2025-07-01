from flask import Flask, request, jsonify
import sqlite3
import os

DB_PATH = r'food.db'
TABLE_NAME = 'basement_freezer'
COLUMNS = ['item', 'dateofpurchase', 'weight', 'amount']

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/items', methods=['GET'])
def get_items():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT rowid, * FROM {TABLE_NAME}')
    rows = cur.fetchall()
    conn.close()
    items = []
    for row in rows:
        item = {col: row[col] for col in COLUMNS}
        item['rowid'] = row['rowid']
        items.append(item)
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    values = [data.get(col, '') for col in COLUMNS]
    conn = get_db_connection()
    cur = conn.cursor()
    placeholders = ', '.join(['?'] * len(COLUMNS))
    cur.execute(f'INSERT INTO {TABLE_NAME} ({', '.join(COLUMNS)}) VALUES ({placeholders})', values)
    conn.commit()
    rowid = cur.lastrowid
    conn.close()
    return jsonify({'rowid': rowid}), 201

@app.route('/items/<int:rowid>', methods=['PUT'])
def update_item(rowid):
    data = request.json
    values = [data.get(col, '') for col in COLUMNS]
    conn = get_db_connection()
    cur = conn.cursor()
    set_clause = ', '.join([f'{col}=?' for col in COLUMNS])
    cur.execute(f'UPDATE {TABLE_NAME} SET {set_clause} WHERE rowid=?', (*values, rowid))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/items/<int:rowid>', methods=['DELETE'])
def delete_item(rowid):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {TABLE_NAME} WHERE rowid=?', (rowid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print(f'Database not found at {DB_PATH}')
    else:
        app.run(debug=True) 