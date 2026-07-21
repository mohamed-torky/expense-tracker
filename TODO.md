# Project Refactoring TODO

## Phase 1: Fix Critical Bugs
- [ ] Fix `notes = notes = input(...)` duplicate assignment in main.py
- [ ] Fix `db4 = database` (assigns class, not instance) in main.py
- [ ] Wrap main execution in `if __name__ == "__main__":`
- [ ] Remove hardcoded `sys.path.append` in database.py
- [ ] Remove module-level `os.chdir` side effect in models.py

## Phase 2: Refactor Architecture
- [ ] Rewrite models.py as proper database connection manager
- [ ] Rewrite database.py as ExpenseRepository with clean separation
- [ ] Rewrite main.py with proper structure and functions

## Phase 3: Add New Features
- [ ] Add search expenses by keyword
- [ ] Add filter by category
- [ ] Add sort functionality
- [ ] Add CSV export
- [ ] Add statistics (total, average, min, max)
- [ ] Add colored terminal output
- [ ] Add input validation helpers

## Phase 4: Security & Best Practices
- [ ] Add proper logging instead of print statements
- [ ] Add validation (negative amounts, empty strings)
- [ ] Use context managers for DB connections
- [ ] Improve error handling with specific exceptions

