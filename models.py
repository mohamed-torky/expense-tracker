import sqlite3
import os
import datetime

# Change the current working directory to the project directory
os.chdir(os.path.dirname(__file__))

# Database connection
db = sqlite3.connect("expense.db")
cr = db.cursor()

# Today's date
today = datetime.date.today().isoformat()


def save_and_close():
    """
    Save all changes to the database.
    """
    db.commit()
    print("Changes saved successfully.")


def close_connection():
    """
    Save changes and close the database connection.
    """
    db.commit()
    db.close()
    print("Database connection closed.")