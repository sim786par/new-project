# API Endpoints
from fastapi import APIRouter
from models import SessionData, UserStats
from carbon_calculator import calculate_co2
from app_classifier import classify_app
from datetime import datetime
import sqlite3

from fastapi import APIRouter, HTTPException
from models import SessionData
from carbon_calculator import calculate_co2
from datetime import datetime
import sqlite3

router = APIRouter()

@router.post("/receive_data")
async def receive_data(data: SessionData):
    try:
        conn = sqlite3.connect("carbon_tracker.db")
        cursor = conn.cursor()

        # Convert session duration min -> seconds
        screen_time_sec = int(data.session_duration_min * 60)

        # Total network data in MB
        data_mb = (data.network_sent + data.network_recv) / (1024*1024)

        # Auto calculate CO2
        co2_grams = calculate_co2(data.cpu_usage, data.ram_usage, data_mb)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO sessions 
            (user_id, cpu_usage, ram_usage, disk_usage,
             network_sent, network_recv, active_connections,
             app_name, screen_time_seconds, co2_grams, network_type, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.user_id,
            data.cpu_usage,
            data.ram_usage,
            0,                       # disk_usage
            data.network_sent,
            data.network_recv,
            0,                       # active_connections
            data.active_app,         # app_name
            screen_time_sec,
            co2_grams,
            data.network_type,
            timestamp
        ))

        conn.commit()
        conn.close()

        return {"message": "Data saved successfully", "co2_grams": round(co2_grams,2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats/{user_id}")
async def get_stats(user_id: str):

    conn = sqlite3.connect("carbon_tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            SUM(co2_grams),
            AVG(cpu_usage),
            AVG(ram_usage),
            SUM(network_sent + network_recv),
            SUM(screen_time_seconds)
        FROM sessions
        WHERE user_id = ?
    """, (user_id,))

    result = cursor.fetchone()
    total_co2, avg_cpu, avg_ram, total_network, total_screen_time = result

    if total_co2 is None:
        conn.close()
        return {"message": "No data found"}

    total_data_mb = (total_network or 0) / (1024 * 1024)

    # Top 5 apps by screen time
    cursor.execute("""
        SELECT app_name, SUM(screen_time_seconds) as total_time
        FROM sessions
        WHERE user_id = ?
        GROUP BY app_name
        ORDER BY total_time DESC
        LIMIT 5
    """, (user_id,))

    top_apps = [{"app_name": row[0], "screen_time_seconds": row[1]} for row in cursor.fetchall()]

    conn.close()

    return {
        "user_id": user_id,
        "total_co2_grams": round(total_co2 or 0, 2),
        "average_cpu_percent": round(avg_cpu or 0, 2),
        "average_ram_percent": round(avg_ram or 0, 2),
        "total_data_used_mb": round(total_data_mb, 2),
        "total_screen_time_seconds": total_screen_time or 0,
        "top_5_most_used_apps": top_apps
    }