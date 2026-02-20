import sqlite3

conn = sqlite3.connect("carbon_tracker.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    cpu_usage REAL,
    ram_usage REAL,
    disk_usage REAL,
    network_sent REAL,
    network_recv REAL,
    active_connections INTEGER,
    app_name TEXT,
    screen_time_seconds INTEGER,
    co2_grams REAL,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

print("Database and sessions table created successfully!")