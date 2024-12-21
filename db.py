import sqlite3

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def get_vehicles():
    conn = get_db_connection()
    vehicles = conn.execute('SELECT * FROM Vehicles').fetchall()
    conn.close()
    return vehicles

def get_bookings():
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM Bookings').fetchall()
    conn.close()
    return bookings