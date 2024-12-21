from flask import Flask, render_template
import db

app = Flask(__name__)

@app.route("/")
def index():
    vehicles = db.get_vehicles()
    return render_template('index.html', vehicles=vehicles)

@app.route("/bookings")
def bookings():
    bookings = db.get_bookings()
    return render_template('bookings.html', bookings=bookings)

if __name__ == "__main__":
    app.run(debug=True)