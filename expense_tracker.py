# Import our database
import database

def main():
    while True:
        print("\n Expense Tracker Menu")
        print("1. Add Expense")
        print("2. View Expense")
        print("3. Update Expense")
        print("4. Delete Expense")
        print("5. Exit")

        choice = input("Enter your option (1 - 5): ")

        if choice == "1":
            add_expense_cli()
        elif choice == "2":
            view_expense_cli()
        elif choice == "3":
            update_expense_cli()
        elif choice == "4":
            delete_expense_cli()
        elif choice == "5":
            print("Exiting Program. Goodbye!")
            break
        else:
            print("Invalid Choice. Please select a number between 1 and 5")

# Function to add an expense through the CLI
def add_expense_cli():
    date = input("Enter the date of the expense (YYYY-MM-DD): ")
    category = input("Enter the category of the expense: ")
    description = input("Enter the description of the expense: ")
    try:
        amount = float(input("Enter the amount of the expense: "))

        database.add_expense(date, category, description, amount)
    except ValueError:
        print("Invalid Amount. Please enter a numeric value")

# Function to view all expenses through the CLI
def view_expense_cli():
    expenses = database.get_expenses()

    if len(expenses) == 0:
        print("No expenses found.")
    else:
        for expense in expenses:
            print(f"ID: {expense[0]}")
            print(f"Date: {expense[1]}")
            print(f"Category: {expense[2]}")
            print(f"Description: {expense[3]}")
            print(f"Amount: {expense[4]}")
            print("")  # Empty line for spacing

# Function to update an expense through the CLI
def update_expense_cli():
    view_expense_cli()

    try:
        expense_id = int(input("Enter the ID of the expense you want to update: "))
        date = input("Enter the new date of the expense (YYYY-MM-DD): ")
        category = input("Enter the new category of the expense: ")
        description = input("Enter the new description of the expense: ")
        amount = float(input("Enter the new amount of the expense: "))

        new_data = {
            "date": date,
            "category": category,
            "description": description,
            "amount": amount
        }

        database.update_expense(expense_id, new_data)
    except ValueError:
        print("Invalid ID or Amount. Please enter a numeric value")

# Function to delete an expense through the CLI
def delete_expense_cli():
    view_expense_cli()

    try:
        expense_id = int(input("Enter the ID of the expense you want to delete: "))
        database.delete_expense(expense_id)
    except ValueError:
        print("Invalid ID. Please enter a numeric value")