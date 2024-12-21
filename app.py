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

@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = db.get_db_connection()
    try:
      conn.execute('DELETE FROM Bookings WHERE BookingID = ?', (id,))
      conn.commit()
      flash('"{}" was successfully deleted!'.format(id))
    except sqlite3.Error as e:
      flash(f'Error deleting record: {e}')
    finally:
      conn.close()
    return redirect(url_for('bookings'))

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    booking = db.get_booking(id)

    if booking is None:
        flash('Booking not found.')
        return redirect(url_for('bookings'))

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
                vehicle_id = int(vehicle_id)
            except ValueError:
                flash('Invalid Vehicle ID')
                return render_template('edit.html', booking=booking)

            conn = db.get_db_connection()
            try:
                conn.execute('UPDATE Bookings SET VehicleID = ?, BookingDate = ?, CustomerName = ?, ContactInfo = ?'
                             ' WHERE BookingID = ?', (vehicle_id, booking_date, customer_name, contact_info, id))
                conn.commit()
                flash('Booking successfully updated')
            except sqlite3.IntegrityError:
                flash('Vehicle with this ID does not exist')
                conn.close()
                return render_template('edit.html', booking=booking)
            finally:
                conn.close()

            return redirect(url_for('bookings'))

    return render_template('edit.html', booking=booking)

if __name__ == "__main__":
    app.run(debug=True)