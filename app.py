from flask import Flask, render_template, request, redirect, url_for, flash
import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # Required for flash messages

@app.route("/")
def index():
    vehicles = db.get_vehicles()
    return render_template('index.html', vehicles=vehicles)

@app.route("/bookings")
def bookings():
    bookings = db.get_bookings()
    return render_template('bookings.html', bookings=bookings)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        vehicle_id = request.form['vehicle_id']
        booking_date = request.form['booking_date']
        customer_name = request.form['customer_name']
        contact_info = request.form['contact_info']

        if not vehicle_id:
            flash('Vehicle ID is required!')
        elif not booking_date:
            flash('Booking date is required!')
        elif not customer_name:
            flash('Customer name is required!')
        elif not contact_info:
            flash('Contact info is required!')
        else:
            try:
                vehicle_id = int(vehicle_id) # Try to convert to integer
            except ValueError:
                flash('Invalid Vehicle ID')
                return render_template('create_booking.html')

            conn = db.get_db_connection()
            try:
                conn.execute('INSERT INTO Bookings (VehicleID, BookingDate, CustomerName, ContactInfo) VALUES (?, ?, ?, ?)',
                         (vehicle_id, booking_date, customer_name, contact_info))
                conn.commit()
                conn.close()
                return redirect(url_for('bookings'))
            except sqlite3.IntegrityError:
                flash('Vehicle with this ID does not exist')
                conn.close()
                return render_template('create_booking.html')

        return render_template('create_booking.html')
    return render_template('create_booking.html')

if __name__ == "__main__":
    app.run(debug=True)