
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta, timezone

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "detection_history.db"

# Indian Standard Time (UTC+5:30); no external timezone data required.
IST = timezone(timedelta(hours=5, minutes=30))


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS detection_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                face_count INTEGER NOT NULL,
                status TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS detected_faces (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                confidence REAL NOT NULL
            )
        """)


def get_detection_history(limit=10):
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT id, timestamp, face_count, status
            FROM detection_history
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return rows


def save_detected_face(confidence):
    with get_connection() as connection:
        cursor = connection.execute("""
            INSERT INTO detected_faces (confidence)
            VALUES (?)
        """, (float(confidence),))

        record_id = cursor.lastrowid

        row = connection.execute("""
            SELECT timestamp
            FROM detected_faces
            WHERE id = ?
        """, (record_id,)).fetchone()

    return {
        "face_id": f"FACE-{record_id:06d}",
        "timestamp": row["timestamp"],
        "confidence": float(confidence)
    }


def get_detected_faces(limit=20):
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT id, timestamp, confidence
            FROM detected_faces
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return [
        {
            "face_id": f"FACE-{row['id']:06d}",
            "timestamp": row["timestamp"],
            "confidence": row["confidence"]
        }
        for row in rows
    ]


def get_dashboard_stats():
    with get_connection() as connection:
        image_stats = connection.execute("""
            SELECT
                COUNT(*) AS total_images,
                COALESCE(SUM(face_count), 0) AS total_faces,
                COALESCE(
                    SUM(
                        CASE
                            WHEN face_count = 0 THEN 1
                            ELSE 0
                        END
                    ),
                    0
                ) AS images_without_faces
            FROM detection_history
            WHERE status = 'Success'
        """).fetchone()

        face_stats = connection.execute("""
            SELECT
                COUNT(*) AS recorded_faces,
                AVG(confidence) AS average_confidence
            FROM detected_faces
        """).fetchone()

    average_confidence = face_stats["average_confidence"]

    return {
        "total_images": image_stats["total_images"],
        "total_faces": image_stats["total_faces"],
        "images_without_faces": image_stats["images_without_faces"],
        "recorded_faces": face_stats["recorded_faces"],
        "average_confidence": (
            average_confidence * 100
            if average_confidence is not None
            else None
        )
    }


def get_daily_activity(days=7):
    # Use IST to determine the current calendar date.
    today = datetime.now(IST).date()
    start_date = today - timedelta(days=days - 1)

    with get_connection() as connection:
        rows = connection.execute("""
            SELECT
                date(timestamp, '+330 minutes') AS activity_date,
                COUNT(*) AS images,
                COALESCE(SUM(face_count), 0) AS faces
            FROM detection_history
            WHERE status = 'Success'
              AND date(timestamp, '+330 minutes') >= ?
              AND date(timestamp, '+330 minutes') <= ?
            GROUP BY date(timestamp, '+330 minutes')
            ORDER BY activity_date
        """, (
            start_date.isoformat(),
            today.isoformat()
        )).fetchall()

    activity_by_date = {
        row["activity_date"]: {
            "images": row["images"],
            "faces": row["faces"]
        }
        for row in rows
    }

    activity = []

    for offset in range(days):
        current_date = start_date + timedelta(days=offset)

        values = activity_by_date.get(
            current_date.isoformat(),
            {"images": 0, "faces": 0}
        )

        activity.append({
            "date": current_date.isoformat(),
            "label": current_date.strftime("%d %b"),
            "images": values["images"],
            "faces": values["faces"]
        })

    return activity
