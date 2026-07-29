import sqlite3


DATABASE_NAME = "complaints.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complaints(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            ticket_id TEXT,

            complaint TEXT,

            location TEXT,
            
            student_email TEXT,

            category TEXT,

            priority TEXT,

            department TEXT,

            status TEXT,

            created_at TEXT
        )
    """
    )
    cursor.execute("PRAGMA table_info(complaints)")

    existing_columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "student_email" not in existing_columns:
        cursor.execute(
            """
            ALTER TABLE complaints
            ADD COLUMN student_email TEXT
            """
        )
    connection.commit()
    connection.close()

def save_complaint(
    ticket_id,
    complaint,
    location,
    student_email,
    category,
    priority,
    department,
    status,
    created_at
):

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO complaints(

            ticket_id,
            complaint,
            location,
            student_email,
            category,
            priority,
            department,
            status,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            ticket_id,
            complaint,
            location,
            student_email,
            category,
            priority,
            department,
            status,
            created_at,
        )
    )

    connection.commit()
    connection.close()

def get_all_complaints():

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            ticket_id,
            complaint,
            location,
            student_email,
            category,
            priority,
            department,
            status,
            created_at
        FROM complaints
        ORDER BY id DESC
    """)

    complaints = cursor.fetchall()

    connection.close()

    return complaints

import sqlite3
from datetime import datetime


DATABASE_NAME = "complaints.db"


def get_next_ticket_number() -> int:
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    today = datetime.now().strftime("%Y%m%d")
    prefix = f"AVVP-{today}-"

    cursor.execute(
        """
        SELECT ticket_id
        FROM complaints
        WHERE ticket_id LIKE ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (f"{prefix}%",),
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return 1

    try:
        last_number = int(row[0].split("-")[-1])
        return last_number + 1
    except (ValueError, IndexError):
        return 1

def update_complaint_status(ticket_id: str, new_status: str) -> None:
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE complaints
        SET status = ?
        WHERE ticket_id = ?
        """,
        (new_status, ticket_id),
    )

    connection.commit()
    connection.close()