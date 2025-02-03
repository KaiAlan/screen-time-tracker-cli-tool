import time
import sqlite3
import win32gui
import win32process
import psutil
from datetime import datetime

DB_NAME = "screen_time.db"

def get_active_app():
    """Get the name of the currently active application."""
    try:
        hwnd = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid)
        return process.name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def track_screen_time():
    """Track screen time and store in SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    current_app = None
    start_time = None

    try:
        while True:
            new_app = get_active_app()
            
            if new_app != current_app:
                # Record previous app session
                if current_app and start_time:
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    
                    conn.execute("""
                        INSERT INTO app_usage 
                        (app_name, start_time, end_time, duration)
                        VALUES (?, ?, ?, ?)
                    """, (current_app, start_time.isoformat(), 
                          end_time.isoformat(), duration))
                    conn.commit()

                # Start new session
                current_app = new_app
                start_time = datetime.now()

            time.sleep(1)

    except KeyboardInterrupt:
        conn.close()

def initialize_database():
    """Create tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS app_usage (
            id INTEGER PRIMARY KEY,
            app_name TEXT NOT NULL,
            start_time DATETIME NOT NULL,
            end_time DATETIME,
            duration INTEGER
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_summary (
            date DATE PRIMARY KEY,
            total_time INTEGER
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_database()  # Add this line before starting the tracker
    track_screen_time()