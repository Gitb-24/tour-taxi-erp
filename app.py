from flask import Flask, render_template, request, redirect, url_for
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

@app.route("/bookings")
def bookings():
  conn = get_db_connection()
  bookings = conn.execute('SELECT * FROM Bookings').fetchall()
  conn.close()
  return render_template('bookings.html', bookings=bookings)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        vehicle_id = request.form['vehicle_id']
        booking_date = request.form['booking_date']
        customer_name = request.form['customer_name']
        contact_info = request.form['contact_info']

        conn = get_db_connection()
        conn.execute('INSERT INTO Bookings (VehicleID, BookingDate, CustomerName, ContactInfo) VALUES (?, ?, ?, ?)',
                     (vehicle_id, booking_date, customer_name, contact_info))
        conn.commit()
        conn.close()
        return redirect(url_for('bookings'))

    return render_template('create_booking.html')

if __name__ == "__main__":
    app.run(debug=True)