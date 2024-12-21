from flask import Flask
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Important for accessing columns by name
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    vehicles = conn.execute('SELECT * FROM Vehicles').fetchall()
    conn.close()
    return f"Hello from your ERP! Vehicles: {vehicles}"

if __name__ == "__main__":
    app.run(debug=True)