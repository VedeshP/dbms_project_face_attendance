import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE attendance ADD COLUMN timestamp TEXT")
    conn.commit()
    print("✅ 'timestamp' column added successfully.")
except sqlite3.OperationalError:
    print("⚠ 'timestamp' column might already exist.")

conn.close()
