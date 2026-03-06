import sqlite3

def create_tables():
    """
    Create all tables for AEDSS if they do not exist.
    """
    conn = sqlite3.connect("aedss.db")
    cursor = conn.cursor()

    # Farmers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS farmers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        gender TEXT,
        crop TEXT,
        farm_size REAL,
        variable_cost REAL,
        fixed_cost REAL,
        yield_amount REAL,
        price REAL
    )
    """)

    conn.commit()
    conn.close()