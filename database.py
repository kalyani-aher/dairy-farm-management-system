import sqlite3

# Connect to the database
connection = sqlite3.connect("dairy_farm.db")

# Create a cursor
cursor = connection.cursor()


# ==================================================
# 🐄 COWS TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS cows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cow_id TEXT UNIQUE,
    breed TEXT,
    age INTEGER
)
""")


# ==================================================
# 🥛 MILK RECORDS TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS milk_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cow_id TEXT,
    date TEXT,
    morning_milk REAL,
    evening_milk REAL,
    total_milk REAL
)
""")


# ==================================================
# 💉 HEALTH RECORDS TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cow_id TEXT,
    record_type TEXT,
    description TEXT,
    date TEXT,
    next_due_date TEXT
)
""")


# ==================================================
# 💰 INCOME & EXPENSES TABLE
# ==================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS finance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_type TEXT,
    category TEXT,
    amount REAL,
    date TEXT,
    description TEXT
)
""")


# ==================================================
# SAVE CHANGES
# ==================================================

connection.commit()


# ==================================================
# CLOSE DATABASE
# ==================================================

connection.close()

print("Database created successfully!")