from flask import Flask, render_template_string, request, redirect, url_for, flash
import sqlite3
import os

DB_PATH = r'food.db'
TABLE_NAME = 'basement_freezer'
COLUMNS = ['item', 'dateofpurchase', 'weight', 'amount']

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Basement Freezer Inventory</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container py-4">
    <h1 class="mb-4">Basement Freezer Inventory</h1>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class="alert alert-info">{{ messages[0] }}</div>
      {% endif %}
    {% endwith %}
    <table class="table table-bordered table-striped">
        <thead>
            <tr>
                {% for col in columns %}
                <th>{{ col }}</th>
                {% endfor %}
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for row in items %}
            <tr>
                {% for col in columns %}
                <td>{{ row[col] }}</td>
                {% endfor %}
                <td>
                    <a href="{{ url_for('edit_item', rowid=row['rowid']) }}" class="btn btn-sm btn-primary">Edit</a>
                    <a href="{{ url_for('delete_item', rowid=row['rowid']) }}" class="btn btn-sm btn-danger" onclick="return confirm('Delete this item?');">Delete</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <a href="{{ url_for('add_item') }}" class="btn btn-success">Add New Item</a>
</div>
</body>
</html>
'''

FORM_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="bg-light">
<div class="container py-4">
    <h2>{{ title }}</h2>
    <form method="post">
        {% for col in columns %}
        <div class="mb-3">
            <label class="form-label">{{ col }}</label>
            {% if col == 'amount' %}
            <input type="number" name="amount" class="form-control" value="{{ values.get('amount', '') }}" min="0" step="1" required>
            {% elif col == 'dateofpurchase' %}
            <input type="date" name="dateofpurchase" class="form-control" value="{{ values.get('dateofpurchase', '') }}" required>
            {% else %}
            <input type="text" name="{{ col }}" class="form-control" value="{{ values.get(col, '') }}" required>
            {% endif %}
        </div>
        {% endfor %}
        <button type="submit" class="btn btn-primary">Save</button>
        <a href="{{ url_for('index') }}" class="btn btn-secondary">Cancel</a>
    </form>
</div>
</body>
</html>
'''

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'SELECT rowid, * FROM {TABLE_NAME}')
    items = cur.fetchall()
    conn.close()
    return render_template_string(TEMPLATE, items=items, columns=COLUMNS)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        values = [request.form.get(col, '') for col in COLUMNS]
        conn = get_db_connection()
        cur = conn.cursor()
        placeholders = ', '.join(['?'] * len(COLUMNS))
        cur.execute(f'INSERT INTO {TABLE_NAME} ({', '.join(COLUMNS)}) VALUES ({placeholders})', values)
        conn.commit()
        conn.close()
        flash('Item added!')
        return redirect(url_for('index'))
    return render_template_string(FORM_TEMPLATE, title='Add Item', columns=COLUMNS, values={})

@app.route('/edit/<int:rowid>', methods=['GET', 'POST'])
def edit_item(rowid):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == 'POST':
        values = [request.form.get(col, '') for col in COLUMNS]
        set_clause = ', '.join([f'{col}=?' for col in COLUMNS])
        cur.execute(f'UPDATE {TABLE_NAME} SET {set_clause} WHERE rowid=?', (*values, rowid))
        conn.commit()
        conn.close()
        flash('Item updated!')
        return redirect(url_for('index'))
    cur.execute(f'SELECT rowid, * FROM {TABLE_NAME} WHERE rowid=?', (rowid,))
    row = cur.fetchone()
    conn.close()
    if not row:
        flash('Item not found!')
        return redirect(url_for('index'))
    values = {col: row[col] for col in COLUMNS}
    return render_template_string(FORM_TEMPLATE, title='Edit Item', columns=COLUMNS, values=values)

@app.route('/delete/<int:rowid>')
def delete_item(rowid):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(f'DELETE FROM {TABLE_NAME} WHERE rowid=?', (rowid,))
    conn.commit()
    conn.close()
    flash('Item deleted!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        print(f'Database not found at {DB_PATH}')
    else:
          app.run(debug=True, host='0.0.0.0')