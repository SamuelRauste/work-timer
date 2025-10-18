import sqlite3

DB_PATH = "work_timer.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS time_logs (
        date TEXT PRIMARY KEY,
        duration TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def log_time(date, duration):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO time_logs (date, duration) VALUES
        (?, ?)
        ON CONFLICT(date) DO UPDATE SET duration = excluded.duration
    """, (date, duration))


    #print(f"logged time {duration} for date {date} in work_timer.db")

    conn.commit()
    conn.close()


def get_all_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM time_logs
    ORDER BY DATE(date) DESC
    """)
    #print("fetched all data from work_timer.db")

    data = cursor.fetchall()
    conn.close()
    print("Here's all data currently in the db: ")
    for i in data:
        print(i)
    return data



