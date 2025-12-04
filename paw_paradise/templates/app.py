from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'pawparadise123'

# 🐾 Initialize Database
def init_db():
    conn = sqlite3.connect('paw_paradise.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT UNIQUE,
                        password TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS services (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT,
                        service_type TEXT,
                        pet_name TEXT,
                        date TEXT,
                        notes TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS adoption (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT,
                        dog_name TEXT,
                        reason TEXT,
                        adoption_date TEXT)''')

    conn.commit()
    conn.close()

init_db()

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('index.html')

# 🧍 Register
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        conn = sqlite3.connect('paw_paradise.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                           (name, email, password))
            conn.commit()
            flash("✅ Registration successful! Please login.")
        except sqlite3.IntegrityError:
            flash("⚠️ Email already exists.")
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

# 🔑 Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('paw_paradise.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            session['user_email'] = user[2]
            session['user_name'] = user[1]
            flash(f"👋 Welcome back, {user[1]}!")
            return redirect(url_for('home'))
        else:
            flash("❌ Invalid email or password.")
            return redirect(url_for('login'))

    return render_template('login.html')

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('home'))

# 🐕 Book Services
@app.route('/book_service', methods=['POST'])
def book_service():
    if 'user_email' not in session:
        flash("Please login to book a service.")
        return redirect(url_for('login'))

    email = session['user_email']
    service_type = request.form['service']
    pet_name = request.form['pet']
    date = request.form['date']
    notes = request.form['notes']

    conn = sqlite3.connect('paw_paradise.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO services (user_email, service_type, pet_name, date, notes) VALUES (?, ?, ?, ?, ?)",
                   (email, service_type, pet_name, date, notes))
    conn.commit()
    conn.close()
    flash("✅ Service booked successfully!")
    return redirect(url_for('view_bookings'))

# 📅 View All Bookings
@app.route('/bookings')
def view_bookings():
    if 'user_email' not in session:
        flash("Please login to view bookings.")
        return redirect(url_for('login'))

    email = session['user_email']
    conn = sqlite3.connect('paw_paradise.db')
    cursor = conn.cursor()
    cursor.execute("SELECT service_type, pet_name, date, notes FROM services WHERE user_email=?", (email,))
    bookings = cursor.fetchall()
    conn.close()

    return render_template('bookings.html', bookings=bookings)

# 🐶 Adoption
@app.route('/adopt', methods=['POST'])
def adopt():
    if 'user_email' not in session:
        flash("Please login to submit adoption request.")
        return redirect(url_for('login'))

    email = session['user_email']
    dog_name = request.form['dog_name']
    reason = request.form['reason']
    adoption_date = request.form['adoption_date']

    conn = sqlite3.connect('paw_paradise.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO adoption (user_email, dog_name, reason, adoption_date) VALUES (?, ?, ?, ?)",
                   (email, dog_name, reason, adoption_date))
    conn.commit()
    conn.close()
    flash("🐾 Adoption request submitted successfully!")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
