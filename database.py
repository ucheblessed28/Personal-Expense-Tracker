import sqlite3
from flask import Flask, render_template, request, redirect, flash, session, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

def create_tables():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT
    )
    ''')
    # Create expenses table with user_id as foreign key
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        category TEXT,
        description TEXT,
        amount REAL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    conn.commit()
    conn.close()

app = Flask(__name__)
app.secret_key = 'c82b4d12a90b3c64735ee3cea1a6e87d4eba69b23a9904585c320524529e5178'
login_manager = LoginManager()
login_manager.init_app(app)

# User model
class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return User(user[0], user[1], user[2]) if user else None

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        conn.close()

        flash("Account created successfully. Please login.")
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("expenses.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            login_user(User(user[0], user[1], user[2]))
            return redirect(url_for('dashboard'))

        flash("Invalid email or password")
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (current_user.id,))
    expenses = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", expenses=expenses)

if __name__ == "__main__":
    app.run(debug=True)



DB_NAME = "expenses.db"

# Database Setup: Create the expenses table if it doesn't exist
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            amount REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database setup complete.")


# Function to add a new expense
def add_expense(date, category, description, amount):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))
    conn.commit()
    conn.close()
    print("Expense added successfully!")

# Function to retrieve all expenses
def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()
    return expenses

# Function to update an existing expense
def update_expense(expense_id, new_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE expenses
        SET date = ?, category = ?, description = ?, amount = ?
        WHERE id = ?
    ''', (new_data["date"], new_data["category"], new_data["description"], new_data["amount"], expense_id))
    conn.commit()
    conn.close()
    print("Expense updated successfully!")

# Function to delete an expense
def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    print("Expense deleted successfully!")

# Run database setup when this script is executed
if __name__ == "__main__":
    setup_database()
