from flask import Flask, request, jsonify
import sqlite3
import os.path
from flask_cors import CORS

db_path = './crud.db'

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:4200", "http://127.0.0.1:4200"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "expose_headers": ["Content-Type", "X-Total-Count"]
    }
})

# Check if the database file exists
check_db = os.path.isfile(db_path)

if not check_db:
    # Create the database file
    print("Database file not found. Creating a new one...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE money_level (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            count_down_date TEXT NOT NULL,
            possiblity TEXT NOT NULL,
            level TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# SQLite database file
DATABASE = './crud.db'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Helper function to connect to the SQLite database
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = dict_factory
    return db

# Create a Money Level Entry (POST) 
@app.route('/money_level', methods=['POST'])
def create_money_level():
    try:
        # Get data from the request
        data = request.json
        if not all(key in data for key in ['date', 'count_down_date', 'possiblity', 'level']):
            return jsonify({"error": "Missing required fields"}), 400

        # Connect to the database
        conn = get_db()
        cursor = conn.cursor()

        # Insert data into the money_level table
        cursor.execute('''
            INSERT INTO money_level (date, count_down_date, possiblity, level)
            VALUES (?, ?, ?, ?)
        ''', (data['date'], data['count_down_date'], data['possiblity'], data['level']))

        # Commit and close the connection
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return jsonify({"id": new_id, "message": "Money level entry created successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all Money Level Entries (GET)
@app.route('/money_level', methods=['GET'])
def get_money_levels():
    try:
        # Connect to the database
        conn = get_db()
        cursor = conn.cursor()

        # Retrieve all records from the table
        cursor.execute('SELECT * FROM money_level')
        money_levels = cursor.fetchall()
        conn.close()

        return jsonify(money_levels), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get a specific Money Level Entry by ID (GET)
@app.route('/money_level/<int:id>', methods=['GET'])
def get_money_level(id):
    try:
        # Connect to the database
        conn = get_db()
        cursor = conn.cursor()

        # Retrieve a specific record from the table
        cursor.execute('SELECT * FROM money_level WHERE id = ?', (id,))
        money_level = cursor.fetchone()
        conn.close()

        if money_level is None:
            return jsonify({"error": "Money level entry not found"}), 404

        return jsonify(money_level), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update a Money Level Entry (PUT)
@app.route('/money_level/<int:id>', methods=['PUT'])
def update_money_level(id):
    try:
        # Get data from the request
        data = request.json
        if not all(key in data for key in ['date', 'count_down_date', 'possiblity', 'level']):
            return jsonify({"error": "Missing required fields"}), 400

        # Connect to the database
        conn = get_db()
        cursor = conn.cursor()

        # Update the record
        cursor.execute('''
            UPDATE money_level 
            SET date = ?, count_down_date = ?, possiblity = ?, level = ?
            WHERE id = ?
        ''', (data['date'], data['count_down_date'], data['possiblity'], data['level'], id))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Money level entry not found"}), 404

        conn.commit()
        conn.close()

        return jsonify({"message": "Money level entry updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a Money Level Entry (DELETE)
@app.route('/money_level/<int:id>', methods=['DELETE'])
def delete_money_level(id):
    try:
        # Connect to the database
        conn = get_db()
        cursor = conn.cursor()

        # Delete the record
        cursor.execute('DELETE FROM money_level WHERE id = ?', (id,))
        
        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "Money level entry not found"}), 404

        conn.commit()
        conn.close()

        return jsonify({"message": "Money level entry deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
