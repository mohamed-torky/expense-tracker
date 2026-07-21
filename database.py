from models import *


class Database:
    """
    A class to manage expense records in the SQLite database.
    """

    def __init__(self, amount=0, category="Some Things", date=today, notes="No notes"):
        self.amount = amount
        self.category = category
        self.date = date
        self.notes = notes

    @staticmethod
    def create_table():
        """
        Create the expenses table if it doesn't already exist.
        """
        cr.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                amount INTEGER,
                category TEXT,
                date TEXT,
                notes TEXT
            )
        """)
        save_and_close()

    def add_expense(self):
        """
        Add a new expense.
        """
        cr.execute("""
            INSERT INTO expenses (amount, category, date, notes)
            VALUES (?, ?, ?, ?)
        """, (self.amount, self.category, self.date, self.notes))

        save_and_close()
        print("\nExpense added successfully.\n")

    def update_expense(self, old_amount, old_category, old_date, old_notes):
        """
        Update an existing expense.
        """
        cr.execute("""
            UPDATE expenses
            SET amount=?,
                category=?,
                date=?,
                notes=?
            WHERE amount=?
            AND category=?
            AND date=?
            AND notes=?
        """, (
            self.amount,
            self.category,
            self.date,
            self.notes,
            old_amount,
            old_category,
            old_date,
            old_notes
        ))

        save_and_close()

        if cr.rowcount:
            print("\nExpense updated successfully.\n")
        else:
            print("\nExpense not found.\n")

    def delete_expense(self):
        """
        Delete an expense.
        """
        cr.execute("""
            DELETE FROM expenses
            WHERE amount=?
            AND LOWER(category)=LOWER(?)
            AND date=?
            AND LOWER(notes)=LOWER(?)
        """, (
            self.amount,
            self.category,
            self.date,
            self.notes
        ))

        save_and_close()

        if cr.rowcount:
            print("\nExpense deleted successfully.\n")
        else:
            print("\nExpense not found.\n")

    @staticmethod
    def view_all():
        """
        Display all expenses.
        """
        cr.execute("SELECT * FROM expenses")
        expenses = cr.fetchall()

        if not expenses:
            print("\nNo expenses found.\n")
            return

        print("\n========== ALL EXPENSES ==========\n")

        total = 0

        for amount, category, date, notes in expenses:
            total += amount

            print(f"Amount   : {amount}")
            print(f"Category : {category}")
            print(f"Date     : {date}")
            print(f"Notes    : {notes}")
            print("-" * 35)

        print(f"Total Expenses = {total}\n")

    @staticmethod
    def view_month(year, month):
        """
        Display all expenses for a specific month.
        """
        cr.execute("""
            SELECT * FROM expenses
            WHERE date LIKE ?
        """, (f"{year}-{month}-%",))

        expenses = cr.fetchall()

        if not expenses:
            print("\nNo expenses found for this month.\n")
            return

        total = 0

        print(f"\n====== Expenses ({year}-{month}) ======\n")

        for amount, category, date, notes in expenses:
            total += amount

            print(f"Amount   : {amount}")
            print(f"Category : {category}")
            print(f"Date     : {date}")
            print(f"Notes    : {notes}")
            print("-" * 35)

        print(f"Monthly Total = {total}\n")