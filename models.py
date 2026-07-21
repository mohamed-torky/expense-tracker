"""
Database connection management module.

Provides a centralized database connection and cursor for the Expense Tracker.
Uses a singleton-like pattern via module-level variables with context management.
"""

import sqlite3
import datetime
import os
import logging
from pathlib import Path
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("expense_tracker.log"),
        logging.StreamHandler() if os.getenv("EXPENSE_DEBUG") else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Database Path Resolution ---
# Use the directory of this file as the base for the database
DB_DIR = Path(__file__).resolve().parent
DB_PATH = DB_DIR / "expense.db"

# --- Database Connection ---
_connection: Optional[sqlite3.Connection] = None
_cursor: Optional[sqlite3.Cursor] = None


def get_connection() -> sqlite3.Connection:
    """Get or create the database connection."""
    global _connection
    if _connection is None:
        try:
            _connection = sqlite3.connect(str(DB_PATH))
            _connection.execute("PRAGMA journal_mode=WAL")
            _connection.execute("PRAGMA foreign_keys=ON")
            logger.info("Database connection established at %s", DB_PATH)
        except sqlite3.Error as e:
            logger.critical("Failed to connect to database: %s", e)
            raise
    return _connection


def get_cursor() -> sqlite3.Cursor:
    """Get or create the database cursor."""
    global _cursor
    if _cursor is None:
        _cursor = get_connection().cursor()
    return _cursor


def save_and_close() -> None:
    """Commit all pending transactions and close the connection gracefully."""
    global _connection, _cursor
    try:
        if _connection:
            _connection.commit()
            logger.debug("Database transaction committed.")
    except sqlite3.Error as e:
        logger.error("Error committing transaction: %s", e)
    finally:
        if _cursor:
            _cursor.close()
            _cursor = None
        if _connection:
            _connection.close()
            _connection = None
            logger.info("Database connection closed.")


# --- Shared Constants ---
today: str = str(datetime.datetime.now().date())
db = get_connection()
cr = get_cursor()


class DatabaseManager:
    """Context manager for safe database operations."""

    def __enter__(self):
        return get_cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            try:
                get_connection().commit()
            except sqlite3.Error as e:
                logger.error("Commit failed: %s", e)
        else:
            get_connection().rollback()
            logger.error("Transaction rolled back due to: %s", exc_val)
        return False

