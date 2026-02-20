import psutil
import time
import sqlite3
from datetime import datetime
import win32gui


# ------------------------------
# CO2 Calculation Formula
# ------------------------------
def calculate_co2(cpu, ram, data_mb):
    return round((cpu * 0.02) + (ram * 0.01) + (data_mb * 0.05), 4)


# ------------------------------
# Get Foreground App (Window Title)
# ------------------------------
def get_foreground_app():
    window = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(window)


# ------------------------------
# Main Data Collection Function
# ------------------------------
def collect_data():

    conn = sqlite3.connect("carbon_tracker.db")
    cursor = conn.cursor()

    # Create table
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

    user_id = "pc_user"
    screen_time_dict = {}

    print("🚀 PC Carbon Monitor Started...")

    while True:
        try:
            # CPU & RAM
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            # Network usage calculation
            net_before = psutil.net_io_counters()
            time.sleep(2)
            net_after = psutil.net_io_counters()

            sent = net_after.bytes_sent - net_before.bytes_sent
            recv = net_after.bytes_recv - net_before.bytes_recv

            connections = len(psutil.net_connections())

            # Foreground App
            app_name = get_foreground_app()

            if not app_name:
                app_name = "Unknown"

            # Screen time tracking
            if app_name not in screen_time_dict:
                screen_time_dict[app_name] = 0

            screen_time_dict[app_name] += 10   # 10 sec loop interval
            screen_time = screen_time_dict[app_name]

            # Data conversion
            data_mb = (sent + recv) / (1024 * 1024)

            # CO2 calculation
            co2 = calculate_co2(cpu, ram, data_mb)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Insert into DB
            cursor.execute("""
            INSERT INTO sessions 
            (user_id, cpu_usage, ram_usage, disk_usage,
             network_sent, network_recv, active_connections,
             app_name, screen_time_seconds, co2_grams, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, cpu, ram, disk,
                sent, recv, connections,
                app_name, screen_time, co2, timestamp
            ))

            conn.commit()

            print(f"""
Saved Data:
CPU: {cpu}%
RAM: {ram}%
Disk: {disk}%
App: {app_name}
Screen Time: {screen_time} sec
CO2: {co2} g
-----------------------------------
""")

            time.sleep(8)  # total approx 10 sec loop

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    collect_data()