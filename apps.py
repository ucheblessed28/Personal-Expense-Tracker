from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import csv  # Import the csv module

app = Flask(__name__)

# Function to connect to database and return dictionary-like objects
def get_db_connection():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row  # Allows access by column name instead of index
    return conn

# Home page to show all expenses
@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    expenses = cursor.fetchall()
    conn.close()
    return render_template("home.html", expenses=expenses)

# Add Expense
@app.route("/add", methods=["POST"])
def add_expense():
    date = request.form["date"]
    category = request.form["category"]
    description = request.form["description"]
    amount = float(request.form["amount"])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO expenses (date, category, description, amount)
        VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))
    conn.commit()
    conn.close()

    return redirect("/")

# DELETE Expense Route
@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Route to export CSV
@app.route('/export_csv')
def export_csv():
    conn = get_db_connection()
    expenses = conn.execute('SELECT date, category, description, amount FROM expenses').fetchall()
    conn.close()

    # CSV File Creation
    csv_filename = "expense_report.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:  # ✅ Use encoding="utf-8"
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Description", "Amount (₦)"])  # CSV headers

        # Format Amounts with commas
        for expense in expenses:
            formatted_amount = f"₦{expense[3]:,.2f}"  # Format amount with commas and 2 decimal places
            writer.writerow([expense[0], expense[1], expense[2], formatted_amount])

    return send_file(csv_filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
