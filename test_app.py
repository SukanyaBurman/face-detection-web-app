import database
import pytest
import io
import sqlite3
import app as face_app
import database


def test_home_page():
    client = face_app.app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Face Detection Studio" in response.data


def test_rejects_text_file():
    client = face_app.app.test_client()

    response = client.post(
        "/detect",
        data={
            "image": (io.BytesIO(b"hello"), "notes.txt")
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Invalid file type" in response.data


def test_rejects_invalid_image():
    client = face_app.app.test_client()

    response = client.post(
        "/detect",
        data={
            "image": (io.BytesIO(b"not a real image"), "photo.jpg")
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200
    assert b"Invalid image" in response.data


def test_database_initialization():
    database.initialize_database()

    with database.get_connection() as connection:
        result = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'detection_history'
        """).fetchone()

    assert result is not None


def test_detection_history_retrieval():
    history = database.get_detection_history(limit=10)

    assert isinstance(history, list)

def test_save_detected_face_unique_id_timestamp_confidence(
    tmp_path, monkeypatch
):
    # Use a separate temporary database for this test
    test_db = tmp_path / "test_detection_history.db"
    monkeypatch.setattr(database, "DATABASE_PATH", test_db)

    database.initialize_database()

    # Save two face records
    first_face = database.save_detected_face(0.984)
    second_face = database.save_detected_face(0.957)

    # Verify that each face gets a unique ID
    assert first_face["face_id"].startswith("FACE-")
    assert second_face["face_id"].startswith("FACE-")
    assert first_face["face_id"] != second_face["face_id"]

    # Verify timestamps are returned
    assert first_face["timestamp"]
    assert second_face["timestamp"]

    # Verify confidence scores
    assert first_face["confidence"] == pytest.approx(0.984)
    assert second_face["confidence"] == pytest.approx(0.957)

    # Verify the records can be retrieved from SQLite
    saved_faces = database.get_detected_faces(limit=10)
    assert len(saved_faces) == 2

    records_by_id = {
        face["face_id"]: face for face in saved_faces
    }

    saved_first = records_by_id[first_face["face_id"]]

    assert saved_first["timestamp"] == first_face["timestamp"]
    assert saved_first["confidence"] == pytest.approx(0.984)
