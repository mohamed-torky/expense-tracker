from database import Database
from models import today, close_connection
import datetime


def clean_text(value, default):
    """
    Return the default value if the user enters nothing,
    otherwise return the formatted text.
    """
    value = value.strip()

    if value == "" or value.lower() == "enter":
        return default

    return value.capitalize()


def get_date():
    """
    Ask the user for a date and validate it.
    Press Enter to use today's date.
    """
    while True:
        date = input(f"Enter the date (YYYY-MM-DD) [Default: {today}]: ").strip()

        if not date:
            return today

        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date format. Please try again.")


def add_expense():
    """
    Add a new expense.
    """
    while True:
        try:
            amount = int(input("Enter the amount: "))

            category = clean_text(
                input("Enter category: "),
                "Some Things"
            )

            date = get_date()

            notes = clean_text(
                input("Enter notes: "),
                "No notes"
            )

            expense = Database(amount, category, date, notes)
            expense.add_expense()

            break

        except ValueError:
            print("Amount must be a number.")


def update_expense():
    """
    Update an existing expense.
    """
    try:
        print("\n----- Old Expense -----")

        old_amount = int(input("Amount: "))
        old_category = clean_text(input("Category: "), "Some Things")
        old_date = get_date()
        old_notes = clean_text(input("Notes: "), "No notes")

        print("\n----- New Expense -----")

        new_amount = int(input("Amount: "))
        new_category = clean_text(input("Category: "), "Some Things")
        new_date = get_date()
        new_notes = clean_text(input("Notes: "), "No notes")

        expense = Database(
            new_amount,
            new_category,
            new_date,
            new_notes
        )

        expense.update_expense(
            old_amount,
            old_category,
            old_date,
            old_notes
        )

    except ValueError:
        print("Amount must be a number.")


def delete_expense():
    """
    Delete an expense.
    """
    try:
        amount = int(input("Amount: "))
        category = clean_text(input("Category: "), "Some Things")
        date = get_date()
        notes = clean_text(input("Notes: "), "No notes")

        expense = Database(
            amount,
            category,
            date,
            notes
        )

        expense.delete_expense()

    except ValueError:
        print("Amount must be a number.")


def view_month():
    """
    Display expenses for a specific month.
    """
    while True:
        year = input("Enter year (YYYY): ").strip()
        month = input("Enter month (1-12): ").strip()

        if month.isdigit() and 1 <= int(month) <= 12:
            month = month.zfill(2)
            break

        print("Invalid month. Please enter a value between 1 and 12.")

    Database.view_month(year, month)


def exit_program():
    """
    Close database connection and exit.
    """
    close_connection()
    print("\nThank you for using Expense Tracker ❤️")


def menu():
    """
    Display the menu and return the user's choice.
    """
    print("""
========== Expense Tracker ==========

a -> Add Expense
u -> Update Expense
d -> Delete Expense
v -> View All Expenses
m -> View Monthly Expenses
e -> Exit

=====================================
""")

    return input("Choose an option: ").strip().lower()


def main():
    """
    Main program.
    """
    Database.create_table()

    while True:
        choice = menu()

        if choice == "a":
            add_expense()

        elif choice == "u":
            update_expense()

        elif choice == "d":
            delete_expense()

        elif choice == "v":
            Database.view_all()

        elif choice == "m":
            view_month()

        elif choice == "e":
            exit_program()
            break

        else:
            print("\nInvalid option. Please try again.\n")


if __name__ == "__main__":
    main()