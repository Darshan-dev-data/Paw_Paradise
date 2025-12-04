from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

# ✅ Setup Flask
TEMPLATE_DIR = r"C:\Users\pavan\Desktop\paw_paradise\templates"
app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = 'pawparadise123'

# ✅ Initialize Database
def init_db():
    conn = sqlite3.connect('paw_paradise.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT UNIQUE,
                        password TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS services(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_email TEXT,
                        service_type TEXT,
                        pet_name TEXT,
                        date TEXT,
                        notes TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS adoption(
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

# 🧍 Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('paw_paradise.db')
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            flash("Registration successful! Please login.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Email already exists.")
        finally:
            conn.close()
    return render_template('register.html')

# 🔑 Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('paw_paradise.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            flash("Login successful!")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password.")
            return redirect(url_for('login'))
    return render_template('login.html')


# 🐶 Adoption Page
@app.route('/adoption')
def adoption():
    return render_template('adoption_user.html')

# 💇 Grooming Page
@app.route('/grooming')
def grooming():
    return render_template('grooming.html')

# @app.route('/services')
# def services():
#     return render_template('services.html')

@app.route('/services')
def services():
    return render_template('services.html')



# 📞 Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# ℹ️ About Page
@app.route('/about')
def about():
    return render_template('about.html')

# 🐕 Book Service Form
@app.route('/book_service', methods=['POST'])
def book_service():
    email = request.form['email']
    service_type = request.form['service']
    pet_name = request.form['pet']
    date = request.form['date']
    notes = request.form['notes']

    conn = sqlite3.connect('paw_paradise.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO services (user_email, service_type, pet_name, date, notes) VALUES (?, ?, ?, ?, ?)",
        (email, service_type, pet_name, date, notes)
    )
    conn.commit()
    conn.close()
    flash("Service booked successfully!")
    return redirect(url_for('home'))

# 🐾 Adoption Form Submission
@app.route('/adopt', methods=['POST'])
def adopt():
    email = request.form['email']
    dog_name = request.form['dog_name']
    reason = request.form['reason']
    adoption_date = request.form['adoption_date']

    conn = sqlite3.connect('paw_paradise.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO adoption (user_email, dog_name, reason, adoption_date) VALUES (?, ?, ?, ?)",
        (email, dog_name, reason, adoption_date)
    )
    conn.commit()
    conn.close()
    flash("Adoption request submitted successfully!")
    return redirect(url_for('home'))

# ✅ Run Flask App
if __name__ == '__main__':
    print("✅ Flask is running and looking for templates in:", app.template_folder)
app.run(host='0.0.0.0', port=5000, debug=True)
