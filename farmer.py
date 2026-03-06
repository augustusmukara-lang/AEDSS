import sqlite3

DB = "aedss.db"

# -----------------------
# Add Farmer
# -----------------------
def add_farmer(name, gender, crop, farm_size, variable_cost, fixed_cost, yield_amount, price):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO farmers(name, gender, crop, farm_size, variable_cost, fixed_cost, yield_amount, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, gender, crop, farm_size, variable_cost, fixed_cost, yield_amount, price))
    conn.commit()
    conn.close()

# -----------------------
# View Farmers
# -----------------------
def view_farmers():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row  # allows dict-like access
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farmers")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# -----------------------
# Delete Farmer
# -----------------------
def delete_farmer(farmer_id):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM farmers WHERE id = ?", (farmer_id,))
    conn.commit()
    conn.close()