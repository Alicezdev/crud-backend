from flask import Flask, request, jsonify
import sqlite3
import os.path

db_path = './crud.db'

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

app = Flask(__name__)

# SQLite database file
#DATABASE = '/home/st50109/domains/alicezdev.com/public_html/Sqlite/sqlite-autoconf-3470000/crud.db'
DATABASE = './crud.db'

# Helper function to connect to the SQLite database
def get_db():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    return db


# Create a Money Level Entry (POST) 
@app.route('/money_level', methods=['POST'])
def create_money_level():
    try:
        # Get data from the request
        date = request.json.get('date')
        count_down_date = request.json.get('count_down_date')
        possiblity = request.json.get('possiblity')
        level = request.json.get('level')

        # Connect to the database
        conn = get_db()
        print(conn)
        cursor = conn.cursor()

        # Insert data into the money_level table
        cursor.execute('''
            INSERT INTO money_level (date, count_down_date, possiblity, level)
            VALUES (?, ?, ?, ?)
        ''', (date, count_down_date, possiblity, level))

        # Commit and close the connection
        conn.commit()
        conn.close()

        return jsonify({"message": "Money level entry created successfully!"}), 201
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

        # Convert query result to a list of dictionaries
        result = [{"id": entry["id"], "date": entry["date"], "count_down_date": entry["count_down_date"],
                   "possiblity": entry["possiblity"], "level": entry["level"]} for entry in money_levels]

        conn.close()

        return jsonify(result), 200
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

        if money_level:
            result = {
                "id": money_level["id"],
                "date": money_level["date"],
                "count_down_date": money_level["count_down_date"],
                "possiblity": money_level["possiblity"],
                "level": money_level["level"]
            }
            conn.close()
            return jsonify(result), 200
        else:
            conn.close()
            return jsonify({"message": "Money level entry not found!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update a Money Level Entry (PUT)
@app.route('/money_level/<int:id>', methods=['PUT'])
def update_money_level(id):
    try:
        # Get data from the request
        date = request.json.get('date')
        count_down_date = request.json.get('count_down_date')
        possiblity = request.json.get('possiblity')
        level = request.json.get('level')

        # Connect to the database
        conn = get_db()
        cursor = conn.cursor()

        # Update the money_level table
        cursor.execute('''
            UPDATE money_level
            SET date = ?, count_down_date = ?, possiblity = ?, level = ?
            WHERE id = ?
        ''', (date, count_down_date, possiblity, level, id))

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

        # Delete the money_level entry from the table
        cursor.execute('DELETE FROM money_level WHERE id = ?', (id,))

        conn.commit()
        conn.close()

        return jsonify({"message": "Money level entry deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
