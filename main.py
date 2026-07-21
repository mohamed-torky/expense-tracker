"""
Expense Tracker - Main Entry Point

A CLI-based personal expense tracker that allows users to:
  - Add, update, delete, and view expenses
  - View expenses for a specific month
  - Search, filter, and sort expenses
  - View statistics and export to CSV

Usage:
    python main.py
"""

import sys
import datetime
from typing import Optional
from database import ExpenseRepository


# ======================================================================
# Input Helpers
# ======================================================================

def get_int_input(prompt: str, allow_zero: bool = False) -> Optional[int]:
    """
    Safely read an integer from the user.

    Args:
        prompt: The prompt to display.
        allow_zero: If True, zero is a valid input.

    Returns:
        The integer value, or None if the user cancels.
    """
    while True:
        raw = input(prompt).strip()
        if raw.lower() in ("exit", "q", "quit"):
            return None
        try:
            value = int(raw)
            if not allow_zero and value <= 0:
                print("⚠️  Amount must be a positive number.")
                continue
            return value
        except ValueError:
            print("❌ Invalid number. Please enter a valid integer.")


def get_date_input(prompt: str) -> Optional[str]:
    """
    Safely read a date string from the user.

    Args:
        prompt: The prompt to display.

    Returns:
        A date string in YYYY-MM-DD format, or None if cancelled.
    """
    while True:
        raw = input(prompt).strip()
        if raw.lower() in ("exit", "q", "quit"):
            return None
        if not raw:
            return str(datetime.date.today())
        try:
            datetime.datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD (e.g., 2024-01-15).")


def get_non_empty_input(prompt: str, default: str = "") -> str:
    """
    Read a non-empty string from the user.

    Args:
        prompt: The prompt to display.
        default: The default value if the user enters nothing.

    Returns:
        The input string.
    """
    raw = input(prompt).strip()
    if not raw:
        return default
    return raw


def confirm_action(prompt: str = "Are you sure? (y/n): ") -> bool:
    """Ask the user for confirmation."""
    return input(prompt).strip().lower() == "y"


def pause() -> None:
    """Pause until the user presses Enter."""
    input("\nPress Enter to continue...")


# ======================================================================
# Main Program Features
# ======================================================================

def add_expense() -> None:
    """Add a new expense record."""
    print("\n" + "=" * 50)
    print("   ➕  ADD NEW EXPENSE")
    print("=" * 50)

    amount = get_int_input("Enter the amount: ")
    if amount is None:
        return

    category = get_non_empty_input(
        "Enter the category (skip for 'Some Things'): ",
        default="Some Things",
    ).capitalize()

    date = get_date_input("Enter the date (YYYY-MM-DD) [default: today]: ")
    if date is None:
        return

    notes = get_non_empty_input(
        "Enter the notes (skip for 'No notes'): ",
        default="No notes",
    ).capitalize()

    repo = ExpenseRepository(amount, category, date, notes)
    repo.add()
    pause()


def update_expense() -> None:
    """Update an existing expense record."""
    print("\n" + "=" * 50)
    print("   ✏️  UPDATE EXPENSE")
    print("=" * 50)
    print("First, enter the OLD data to identify the record:")

    old_amount = get_int_input("Enter the old amount: ")
    if old_amount is None:
        return
    old_category = get_non_empty_input(
        "Enter the old category (skip for 'Some Things'): ",
        default="Some Things",
    )
    old_date = get_date_input("Enter the old date (YYYY-MM-DD): ")
    if old_date is None:
        return
    old_notes = get_non_empty_input(
        "Enter the old notes (skip for 'No notes'): ",
        default="No notes",
    )

    print("\nNow, enter the NEW data:")
    new_amount = get_int_input("Enter the new amount: ")
    if new_amount is None:
        return
    new_category = get_non_empty_input(
        "Enter the new category (skip for 'Some Things'): ",
        default="Some Things",
    ).capitalize()
    new_date = get_date_input("Enter the new date (YYYY-MM-DD) [default: today]: ")
    if new_date is None:
        return
    new_notes = get_non_empty_input(
        "Enter the new notes (skip for 'No notes'): ",
        default="No notes",
    ).capitalize()

    repo = ExpenseRepository(new_amount, new_category, new_date, new_notes)
    repo.update(old_amount, old_category, old_date, old_notes)
    pause()


def delete_expense() -> None:
    """Delete an expense record."""
    print("\n" + "=" * 50)
    print("   🗑️  DELETE EXPENSE")
    print("=" * 50)
    print("Enter the details of the expense to delete:")

    amount = get_int_input("Enter the amount: ")
    if amount is None:
        return
    category = get_non_empty_input(
        "Enter the category (skip for 'Some Things'): ",
        default="Some Things",
    )
    date = get_date_input("Enter the date (YYYY-MM-DD): ")
    if date is None:
        return
    notes = get_non_empty_input(
        "Enter the notes (skip for 'No notes'): ",
        default="No notes",
    )

    if confirm_action("Delete this expense? (y/n): "):
        repo = ExpenseRepository(amount, category, date, notes)
        repo.delete()
    else:
        print("🚫 Deletion cancelled.")
    pause()


def view_all_expenses() -> None:
    """View all expenses with sorting options."""
    print("\n" + "=" * 50)
    print("   📋  ALL EXPENSES")
    print("=" * 50)

    sort_choice = input(
        "Sort by? (d)ate, (a)mount, (c)ategory, (n)otes, (enter)=date: "
    ).strip().lower()

    sort_map = {"d": "date", "a": "amount", "c": "category", "n": "notes"}
    sort_by = sort_map.get(sort_choice, "date")

    order = input("Order? (a)scending / (d)escending [a]: ").strip().lower()
    order_dir = "DESC" if order == "d" else "ASC"

    ExpenseRepository.view_all(sort_by=sort_by, order=order_dir)
    pause()


def view_monthly() -> None:
    """View expenses for a specific month."""
    print("\n" + "=" * 50)
    print("   📅  MONTHLY EXPENSES")
    print("=" * 50)

    month = input("Enter the month (MM, e.g., 01): ").strip()
    year = input("Enter the year (YYYY, e.g., 2024): ").strip()

    ExpenseRepository.view_month(year, month)
    pause()


def search_expenses() -> None:
    """Search expenses by keyword."""
    print("\n" + "=" * 50)
    print("   🔍  SEARCH EXPENSES")
    print("=" * 50)

    keyword = input("Enter search keyword: ").strip()
    if not keyword:
        print("⚠️  Keyword cannot be empty.")
        pause()
        return

    field_choice = input(
        "Search in? (a)ll, (c)ategory, (n)otes, a(m)ount [all]: "
    ).strip().lower()

    field_map = {"a": "all", "c": "category", "n": "notes", "m": "amount"}
    field = field_map.get(field_choice, "all")

    ExpenseRepository.search(keyword, field=field)
    pause()


def view_statistics() -> None:
    """Display expense statistics."""
    print("\n" + "=" * 50)
    print("   📊  EXPENSE STATISTICS")
    print("=" * 50)
    ExpenseRepository.get_statistics()
    pause()


def export_csv() -> None:
    """Export expenses to CSV."""
    print("\n" + "=" * 50)
    print("   📁  EXPORT TO CSV")
    print("=" * 50)
    filepath = input(
        "Enter filename [expenses_export.csv]: "
    ).strip() or "expenses_export.csv"
    ExpenseRepository.export_to_csv(filepath)
    pause()


def list_categories() -> None:
    """List all distinct categories."""
    print("\n" + "=" * 50)
    print("   📂  CATEGORIES")
    print("=" * 50)
    cats = ExpenseRepository.get_categories()
    if cats:
        for i, cat in enumerate(cats, 1):
            print(f"  {i}. {cat}")
    else:
        print("  No categories found.")
    pause()


def view_help() -> None:
    """Display help information."""
    print("""
╔══════════════════════════════════════════════════════════╗
║                 EXPENSE TRACKER - HELP                   ║
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║  Available Commands:                                     ║
║                                                          ║
║  a  - Add a new expense                                  ║
║  u  - Update an existing expense                         ║
║  d  - Delete an expense                                  ║
║  v  - View all expenses (with sorting)                   ║
║  m  - View expenses for a specific month                 ║
║  s  - Search expenses by keyword                         ║
║  t  - View expense statistics                            ║
║  e  - Export expenses to CSV                             ║
║  c  - List all categories                                ║
║  h  - Show this help screen                              ║
║  q  - Quit the application                               ║
║                                                          ║
║  Tip: Type 'exit' or 'q' at any prompt to go back.      ║
╚══════════════════════════════════════════════════════════╝
    """)


def quit_app() -> None:
    """Exit the application gracefully."""
    from models import save_and_close
    print("\n👋 Thank you for using Expense Tracker!")
    save_and_close()
    sys.exit(0)


# ======================================================================
# Menu Display
# ======================================================================

def show_menu() -> None:
    """Display the main menu."""
    print("""
╔══════════════════════════════════════════╗
║         EXPENSE TRACKER v2.0            ║
╠══════════════════════════════════════════╣
║                                          ║
║  (a) ➕ Add expense                      ║
║  (u) ✏️  Update expense                  ║
║  (d) 🗑️  Delete expense                  ║
║  (v) 📋 View all expenses                ║
║  (m) 📅 View monthly expenses            ║
║  (s) 🔍 Search expenses                  ║
║  (t) 📊 Statistics                       ║
║  (e) 📁 Export to CSV                    ║
║  (c) 📂 List categories                  ║
║  (h) ℹ️  Help                            ║
║  (q) 🚪 Quit                            ║
║                                          ║
╚══════════════════════════════════════════╝
    """)


# ======================================================================
# Main Entry Point
# ======================================================================

def main() -> None:
    """Main program loop."""
    # Ensure the expenses table exists on startup
    ExpenseRepository._ensure_table()

    menu_actions = {
        "a": add_expense,
        "u": update_expense,
        "d": delete_expense,
        "v": view_all_expenses,
        "m": view_monthly,
        "s": search_expenses,
        "t": view_statistics,
        "e": export_csv,
        "c": list_categories,
        "h": view_help,
        "q": quit_app,
    }

    while True:
        show_menu()
        choice = input("Choose an option: ").strip().lower()

        action = menu_actions.get(choice)
        if action:
            action()
        else:
            print("❌ Invalid option. Type 'h' for help or 'q' to quit.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting...")
        quit_app()
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        from models import save_and_close
        save_and_close()
        sys.exit(1)

