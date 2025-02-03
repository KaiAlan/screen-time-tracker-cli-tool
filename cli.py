import sqlite3
import argparse
from datetime import datetime, timedelta
import os
import time

DB_NAME = "screen_time.db"

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'=' * 40}")
    print(f" {title.upper()} ".center(40, '='))
    print(f"{'=' * 40}\n")

def get_connection():
    """Create and return a database connection."""
    return sqlite3.connect(DB_NAME)

def show_live_dashboard():
    """Show real-time dashboard."""
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            conn = get_connection()
            
            # Today's summary
            today = datetime.now().strftime("%Y-%m-%d")
            total_time = conn.execute("""
                SELECT SUM(duration) FROM app_usage
                WHERE DATE(start_time) = ?
            """, (today,)).fetchone()[0] or 0
            
            # Top apps today
            top_apps = conn.execute("""
                SELECT app_name, SUM(duration) 
                FROM app_usage 
                WHERE DATE(start_time) = ?
                GROUP BY app_name 
                ORDER BY SUM(duration) DESC 
                LIMIT 5
            """, (today,)).fetchall()

            print_header("live dashboard")
            print(f"📅 {today} | ⏳ Total: {seconds_to_hms(total_time)}")
            print("\n🏆 Top Applications:")
            for app, duration in top_apps:
                print(f"  {app[:30]:<30} {seconds_to_hms(duration)}")
            
            print("\n🔄 Refreshing every 5 seconds... (Ctrl+C to exit)")
            time.sleep(5)
            
    except KeyboardInterrupt:
        conn.close()

def generate_report(days=7):
    """Generate weekly report."""
    conn = get_connection()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    data = conn.execute("""
        SELECT DATE(start_time) as date, 
               SUM(duration) as total_time,
               app_name,
               SUM(duration) as app_time
        FROM app_usage
        WHERE DATE(start_time) BETWEEN ? AND ?
        GROUP BY date, app_name
        ORDER BY date DESC, app_time DESC
    """, (start_date.strftime("%Y-%m-%d"), 
          end_date.strftime("%Y-%m-%d"))).fetchall()

    print_header(f"{days}-day report")
    current_date = None
    for row in data:
        date_str, total, app, app_time = row
        if date_str != current_date:
            print(f"\n📅 {date_str} | Total: {seconds_to_hms(total)}")
            current_date = date_str
        print(f"  {app[:30]:<30} {seconds_to_hms(app_time)}")

def seconds_to_hms(seconds):
    """Convert seconds to hours:minutes:seconds format."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}h {int(m):02d}m {int(s):02d}s"

def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Screen Time Tracker CLI Tool")
    
    subparsers = parser.add_subparsers(dest="command")

    # Live dashboard command
    subparsers.add_parser("live", help="Show live dashboard")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate report")
    report_parser.add_argument(
        "--days", type=int, default=7,
        help="Number of days to include in report")

    args = parser.parse_args()

    if args.command == "live":
        show_live_dashboard()
    elif args.command == "report":
        generate_report(args.days)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()