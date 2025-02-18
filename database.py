import sqlite3

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
