"""
Expense Repository module.

Provides a clean repository layer for all database operations
related to expenses. Separates data access logic from business logic.
"""

import logging
import sqlite3
from typing import List, Optional, Tuple
from models import cr, today, logger, DatabaseManager


# Default constants
DEFAULT_CATEGORY = "Some Things"
DEFAULT_NOTES = "No notes"


class ExpenseRepository:
    """
    Repository class for expense database operations.
    Follows the Repository pattern - encapsulates database access logic.
    """

    def __init__(
        self,
        amount: int = 0,
        category: str = DEFAULT_CATEGORY,
        date: str = today,
        notes: str = DEFAULT_NOTES,
    ):
        """
        Initialize an expense record.

        Args:
            amount: The expense amount in your local currency.
            category: The expense category (e.g. Food, Transport).
            date: The date of the expense (YYYY-MM-DD format).
            notes: Optional notes for the expense.
        """
        self.amount = amount
        self.category = category or DEFAULT_CATEGORY
        self.date = date or today
        self.notes = notes or DEFAULT_NOTES

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @staticmethod
    def validate_amount(value: int) -> bool:
        """Check that the amount is a positive integer."""
        if not isinstance(value, int):
            return False
        if value <= 0:
            return False
        return True

    @staticmethod
    def validate_date(date_str: str) -> bool:
        """Validate that the date string follows YYYY-MM-DD."""
        import datetime
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except (ValueError, TypeError):
            return False

    # ------------------------------------------------------------------
    # Schema Management
    # ------------------------------------------------------------------

    @staticmethod
    def _ensure_table() -> None:
        """Create the expenses table if it does not exist."""
        cr.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount INTEGER NOT NULL,
                category TEXT NOT NULL DEFAULT 'Some Things',
                date TEXT NOT NULL,
                notes TEXT DEFAULT 'No notes',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

    # ------------------------------------------------------------------
    # CRUD Operations
    # ------------------------------------------------------------------

    def add(self) -> int:
        """
        Insert a new expense record.

        Returns:
            The rowid of the newly inserted record.
        """
        self._ensure_table()
        try:
            cr.execute(
                "INSERT INTO expenses (amount, category, date, notes) VALUES (?, ?, ?, ?)",
                (self.amount, self.category, self.date, self.notes),
            )
            ExpenseRepository._commit()
            row_id = cr.lastrowid
            logger.info(
                "Expense added [id=%s]: %s %s %s %s",
                row_id, self.amount, self.category, self.date, self.notes,
            )
            print(
                f"✅ Expense added successfully!\n"
                f"   Amount: {self.amount}\n"
                f"   Category: {self.category}\n"
                f"   Date: {self.date}\n"
                f"   Notes: {self.notes}"
            )
            return row_id
        except sqlite3.Error as e:
            logger.error("Failed to add expense: %s", e)
            print(f"❌ Database error: {e}")
            raise

    def update(self, old_amount: int, old_category: str, old_date: str, old_notes: str) -> bool:
        """
        Update an existing expense record.

        Args:
            old_amount: The amount of the record to update.
            old_category: The category of the record to update.
            old_date: The date of the record to update.
            old_notes: The notes of the record to update.

        Returns:
            True if at least one row was updated, False otherwise.
        """
        self._ensure_table()
        try:
            cr.execute(
                """
                UPDATE expenses
                SET amount = ?, category = ?, date = ?, notes = ?
                WHERE amount = ? AND category = ? AND date = ? AND notes = ?
                """,
                (
                    self.amount, self.category, self.date, self.notes,
                    old_amount, old_category or DEFAULT_CATEGORY,
                    old_date, old_notes or DEFAULT_NOTES,
                ),
            )
            ExpenseRepository._commit()
            if cr.rowcount == 0:
                print("⚠️ No matching record found to update.")
                return False
            logger.info("Expense updated: %s rows affected", cr.rowcount)
            print("✅ Expense updated successfully!")
            return True
        except sqlite3.Error as e:
            logger.error("Failed to update expense: %s", e)
            print(f"❌ Database error: {e}")
            return False

    def delete(self) -> bool:
        """
        Delete an expense record matching the current instance data.

        Returns:
            True if a record was deleted, False otherwise.
        """
        self._ensure_table()
        try:
            cr.execute(
                """
                DELETE FROM expenses
                WHERE amount = ?
                  AND LOWER(category) = LOWER(?)
                  AND date = ?
                  AND LOWER(notes) = LOWER(?)
                """,
                (self.amount, self.category, self.date, self.notes),
            )
            ExpenseRepository._commit()
            if cr.rowcount == 0:
                print("⚠️ No matching record found to delete.")
                return False
            logger.info("Expense deleted: %s rows affected", cr.rowcount)
            print("✅ Expense deleted successfully!")
            return True
        except sqlite3.Error as e:
            logger.error("Failed to delete expense: %s", e)
            print(f"❌ Database error: {e}")
            return False

    # ------------------------------------------------------------------
    # Query Operations
    # ------------------------------------------------------------------

    @staticmethod
    def view_all(sort_by: str = "date", order: str = "ASC") -> List[Tuple]:
        """
        Retrieve all expense records.

        Args:
            sort_by: Column to sort by (date, amount, category, notes).
            order: 'ASC' or 'DESC'.

        Returns:
            List of expense tuples.
        """
        ExpenseRepository._ensure_table()
        allowed_sort = {"date", "amount", "category", "notes"}
        sort_col = sort_by if sort_by in allowed_sort else "date"
        order_dir = "ASC" if order.upper() != "DESC" else "DESC"

        try:
            cr.execute(
                f"SELECT id, amount, category, date, notes FROM expenses ORDER BY {sort_col} {order_dir}"
            )
            rows = cr.fetchall()
            ExpenseRepository._commit()

            if not rows:
                print("📭 No expenses found.")
                return []

            print("\n" + "=" * 70)
            print(f"{'ID':<4} {'Amount':<8} {'Category':<18} {'Date':<12} {'Notes':<25}")
            print("-" * 70)
            for row in rows:
                print(f"{row[0]:<4} {row[1]:<8} {row[2]:<18} {row[3]:<12} {row[4]:<25}")
            print("=" * 70)
            logger.info("Viewed all expenses: %s records", len(rows))
            return rows
        except sqlite3.Error as e:
            logger.error("Failed to fetch expenses: %s", e)
            print(f"❌ Database error: {e}")
            return []

    @staticmethod
    def view_month(year: str, month: str) -> float:
        """
        View expenses for a specific month and calculate total.

        Args:
            year: The year (e.g., '2024').
            month: The month (e.g., '01').

        Returns:
            The total amount for the month.
        """
        ExpenseRepository._ensure_table()
        total = 0.0
        try:
            cr.execute(
                "SELECT id, amount, category, date, notes FROM expenses WHERE date LIKE ?",
                (f"{year}-{month}-%",),
            )
            rows = cr.fetchall()
            ExpenseRepository._commit()

            if not rows:
                print(f"📭 No expenses found for {year}-{month}.")
                return 0.0

            print(f"\n--- Expenses for {year}-{month} ---")
            print(f"{'ID':<4} {'Amount':<8} {'Category':<18} {'Date':<12} {'Notes':<25}")
            print("-" * 70)
            for row in rows:
                print(f"{row[0]:<4} {row[1]:<8} {row[2]:<18} {row[3]:<12} {row[4]:<25}")
                total += float(row[1])
            print("-" * 70)
            print(f"📊 Total for {year}-{month}: {total:.2f}")
            logger.info("Monthly view %s-%s: %s records, total=%s", year, month, len(rows), total)
            return total
        except sqlite3.Error as e:
            logger.error("Failed to fetch monthly expenses: %s", e)
            print(f"❌ Database error: {e}")
            return 0.0

    # ------------------------------------------------------------------
    # New Features
    # ------------------------------------------------------------------

    @staticmethod
    def search(keyword: str, field: str = "all") -> List[Tuple]:
        """
        Search expenses by keyword in category, notes, or amount.

        Args:
            keyword: The term to search for.
            field: The field to search ('category', 'notes', 'amount', 'all').

        Returns:
            List of matching expense tuples.
        """
        ExpenseRepository._ensure_table()
        keyword = f"%{keyword}%"
        try:
            if field == "all":
                cr.execute(
                    """
                    SELECT id, amount, category, date, notes FROM expenses
                    WHERE category LIKE ? OR notes LIKE ? OR CAST(amount AS TEXT) LIKE ?
                    """,
                    (keyword, keyword, keyword),
                )
            elif field == "amount":
                cr.execute(
                    "SELECT id, amount, category, date, notes FROM expenses WHERE CAST(amount AS TEXT) LIKE ?",
                    (keyword,),
                )
            else:
                cr.execute(
                    f"SELECT id, amount, category, date, notes FROM expenses WHERE {field} LIKE ?",
                    (keyword,),
                )

            rows = cr.fetchall()
            ExpenseRepository._commit()

            if not rows:
                print(f"🔍 No results for '{keyword.replace('%', '')}'.")
                return []

            print(f"\n--- Search Results for '{keyword.replace('%', '')}' ---")
            for row in rows:
                print(f"  {row[0]:<4} {row[1]:<8} {row[2]:<18} {row[3]:<12} {row[4]:<25}")
            print(f"  ─── {len(rows)} record(s) found ───")
            logger.info("Search for '%s' returned %s results", keyword, len(rows))
            return rows
        except sqlite3.Error as e:
            logger.error("Search failed: %s", e)
            print(f"❌ Database error: {e}")
            return []

    @staticmethod
    def get_statistics() -> dict:
        """
        Calculate statistics for all expenses.

        Returns:
            Dictionary with total, average, min, max, and count.
        """
        ExpenseRepository._ensure_table()
        try:
            cr.execute("""
                SELECT
                    COUNT(*) as count,
                    COALESCE(SUM(amount), 0) as total,
                    COALESCE(AVG(amount), 0) as avg,
                    COALESCE(MIN(amount), 0) as min,
                    COALESCE(MAX(amount), 0) as max
                FROM expenses
            """)
            row = cr.fetchone()
            ExpenseRepository._commit()

            stats = {
                "count": row[0],
                "total": row[1],
                "average": round(row[2], 2),
                "minimum": row[3],
                "maximum": row[4],
            }

            print("\n" + "=" * 45)
            print("📊 EXPENSE STATISTICS")
            print("=" * 45)
            print(f"  Total Expenses : {stats['count']}")
            print(f"  Total Amount   : {stats['total']}")
            print(f"  Average        : {stats['average']}")
            print(f"  Lowest         : {stats['minimum']}")
            print(f"  Highest        : {stats['maximum']}")
            print("=" * 45)
            logger.info("Statistics calculated: %s", stats)
            return stats
        except sqlite3.Error as e:
            logger.error("Statistics failed: %s", e)
            print(f"❌ Database error: {e}")
            return {"count": 0, "total": 0, "average": 0, "minimum": 0, "maximum": 0}

    @staticmethod
    def export_to_csv(filepath: str = "expenses_export.csv") -> bool:
        """
        Export all expenses to a CSV file.

        Args:
            filepath: Destination file path.

        Returns:
            True if export succeeded.
        """
        import csv
        ExpenseRepository._ensure_table()
        try:
            cr.execute("SELECT id, amount, category, date, notes FROM expenses ORDER BY date")
            rows = cr.fetchall()
            ExpenseRepository._commit()

            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Amount", "Category", "Date", "Notes"])
                writer.writerows(rows)

            print(f"📁 Exported {len(rows)} records to '{filepath}'")
            logger.info("Exported %s records to %s", len(rows), filepath)
            return True
        except (sqlite3.Error, OSError, csv.Error) as e:
            logger.error("Export failed: %s", e)
            print(f"❌ Export error: {e}")
            return False

    @staticmethod
    def get_categories() -> List[str]:
        """Retrieve all distinct categories."""
        ExpenseRepository._ensure_table()
        try:
            cr.execute("SELECT DISTINCT category FROM expenses ORDER BY category")
            cats = [row[0] for row in cr.fetchall()]
            return cats
        except sqlite3.Error as e:
            logger.error("Failed to fetch categories: %s", e)
            return []

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _commit() -> None:
        """Commit the current transaction."""
        try:
            cr.connection.commit()
        except sqlite3.Error as e:
            logger.error("Commit failed: %s", e)
            raise

