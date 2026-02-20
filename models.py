from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# -------------------- DATABASE TABLE --------------------

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)

    cpu_usage = Column(Float, nullable=True)
    ram_usage = Column(Float, nullable=True)
    disk_usage = Column(Float, nullable=True)

    network_sent = Column(Float, nullable=True)
    network_recv = Column(Float, nullable=True)
    active_connections = Column(Integer, nullable=True)

    app_name = Column(String, nullable=True)
    screen_time_seconds = Column(Integer, nullable=True)

    co2_grams = Column(Float, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)


# -------------------- REQUEST MODEL --------------------

class SessionData(BaseModel):
    user_id: str
    timestamp: str
    device_type: str
    cpu_usage: float
    ram_usage: float
    network_sent: float
    network_recv: float
    network_type: str            # Ye field tumhara missing tha
    active_app: str
    session_duration_min: float
    battery_percent: float


# -------------------- RESPONSE MODEL --------------------

class UserStats(BaseModel):
    user_id: str
    total_co2_grams: float
    average_cpu_percent: float
    average_ram_percent: float
    total_data_used_mb: float
    total_screen_time_seconds: int
    top_5_most_used_apps: List = Field(default_factory=list)


class UserRegister(BaseModel):
    user_id: str
    username: str


class LeaderboardEntry(BaseModel):
    user_id: str
    total_co2: float
    rank: int


class PredictionResponse(BaseModel):
    predicted_daily_co2: float
    suggestions: List[str]