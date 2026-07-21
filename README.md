# Expense Tracker

A Python-based personal expense tracker that uses SQLite for data persistence. Manage your daily expenses with a clean command-line interface.

## Features

### Core Operations
- **Add** new expenses with amount, category, date, and notes
- **Update** existing expenses
- **Delete** expenses
- **View all** expenses with sorting (by date, amount, category, notes)
- **Monthly view** - see expenses grouped by month with totals

### Advanced Features
- **Search** expenses by keyword across categories, notes, or amounts
- **Statistics** - view total, average, minimum, and maximum expenses
- **Export to CSV** - backup or analyze your data in spreadsheet software
- **Category listing** - see all distinct categories at a glance
- **Sorting** - sort expenses by any field in ascending or descending order

## Technologies

- **Language:** Python 3.8+
- **Database:** SQLite (via `sqlite3` standard library)
- **Logging:** Python `logging` module with file output
- **Paradigm:** Object-Oriented Programming with Repository Pattern

## Installation

1. Ensure Python 3.8+ is installed:

   ```bash
   python --version
   ```

2. Clone or download this repository.

3. No third-party dependencies required! All libraries are from Python's standard library.

## Usage

Run the application:

```bash
python main.py
```

### Menu Options

| Key | Action              | Description                            |
|-----|----------------------|----------------------------------------|
| a   | Add expense          | Add a new expense record               |
| u   | Update expense       | Modify an existing expense             |
| d   | Delete expense       | Remove an expense                      |
| v   | View all expenses    | Display all records with sorting       |
| m   | View monthly         | Show expenses for a specific month     |
| s   | Search               | Find expenses by keyword               |
| t   | Statistics           | View total, average, min, max          |
| e   | Export to CSV        | Export all data to a CSV file          |
| c   | Categories           | List all expense categories            |
| h   | Help                 | Show this help information             |
| q   | Quit                 | Exit the application                   |

## Project Structure

```
expense-tracker/
├── main.py          # Main entry point with CLI interface
├── database.py      # Repository layer with all database operations
├── models.py        # Database connection management and logging config
├── expense.db       # SQLite database file (auto-created)
├── expense_tracker.log  # Application log file (auto-created)
└── README.md        # This file
```

## Architecture

The project follows a clean layered architecture:

```
┌─────────────────────────────────────────────┐
│              main.py (CLI Layer)              │
│  - User interaction & input validation       │
│  - Menu navigation & feature orchestration   │
├─────────────────────────────────────────────┤
│          database.py (Repository Layer)       │
│  - SQL queries & data access                 │
│  - CRUD operations                           │
│  - Search, statistics, export                │
├─────────────────────────────────────────────┤
│          models.py (Connection Layer)         │
│  - Database connection management            │
│  - Logging configuration                     │
│  - Shared constants & context manager        │
└─────────────────────────────────────────────┘
```

## Logging

The application writes logs to `expense_tracker.log` in the same directory. To see logs in the console, set the environment variable:

```bash
set EXPENSE_DEBUG=1    # Windows
export EXPENSE_DEBUG=1 # Linux/Mac
```

## CSV Export

Exported CSV files contain the following columns:
- ID
- Amount
- Category
- Date
- Notes

These can be opened in Excel, Google Sheets, or any spreadsheet software.

## License

MIT License - feel free to use and modify.

