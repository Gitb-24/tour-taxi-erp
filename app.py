from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    conn = get_db_connection()
    vehicles = conn.execute('SELECT * FROM Vehicles').fetchall()
    conn.close()
    return render_template('index.html', vehicles=vehicles)

@app.route("/bookings")  # New route for bookings
def bookings():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM Bookings').fetchall()
    conn.close()
    return render_template('bookings.html', bookings=bookings)

if __name__ == "__main__":
    app.run(debug=True)