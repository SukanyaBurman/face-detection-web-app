
from flask import Flask, render_template, request, Response
import cv2
import numpy as np
import base64
import csv
import io

from pathlib import Path
from datetime import datetime, timezone, timedelta

from database import (
    initialize_database,
    get_connection,
    get_detection_history,
    save_detected_face,
    get_detected_faces,
    get_dashboard_stats,
    get_daily_activity
)


app = Flask(__name__)

initialize_database()

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "face_detection_yunet_2023mar.onnx"

# Indian Standard Time (UTC+5:30).
IST = timezone(timedelta(hours=5, minutes=30))


def format_ist_timestamp(timestamp):
    """Convert a SQLite UTC timestamp into a readable IST timestamp."""
    if not timestamp:
        return ""

    utc_time = datetime.strptime(
        timestamp,
        "%Y-%m-%d %H:%M:%S"
    ).replace(tzinfo=timezone.utc)

    ist_time = utc_time.astimezone(IST)

    return ist_time.strftime("%d-%m-%Y %I:%M:%S %p IST")


def render_home(**kwargs):
    kwargs.setdefault("history", get_detection_history())
    kwargs.setdefault("detected_faces", get_detected_faces())
    kwargs.setdefault("stats", get_dashboard_stats())
    kwargs.setdefault("activity", get_daily_activity())

    kwargs["history"] = [
        {
            **dict(record),
            "timestamp": format_ist_timestamp(record["timestamp"])
        }
        for record in kwargs["history"]
    ]

    kwargs["detected_faces"] = [
        {
            **face,
            "timestamp": format_ist_timestamp(face["timestamp"])
        }
        for face in kwargs["detected_faces"]
    ]

    if kwargs.get("face_results"):
        kwargs["face_results"] = [
            {
                **face,
                "timestamp": format_ist_timestamp(face["timestamp"])
            }
            for face in kwargs["face_results"]
        ]

    return render_template("index.html", **kwargs)


@app.errorhandler(413)
def file_too_large(error):
    return render_home(
        error="Image is too large. Please upload a file smaller than 5 MB."
    ), 413


# Initialize the YuNet face detector.
face_detector = cv2.FaceDetectorYN.create(
    str(MODEL_PATH),
    "",
    (320, 320),
    score_threshold=0.8,
    nms_threshold=0.3,
    top_k=5000
)


@app.route("/")
def home():
    return render_home()


@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return render_home(error="No image was uploaded.")

    file = request.files["image"]

    if file.filename == "":
        return render_home(error="Please select an image.")

    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        return render_home(
            error=(
                "Invalid file type. Please upload a JPG, JPEG, PNG, "
                "or WEBP image."
            )
        )

    image_bytes = file.read()

    if not image_bytes:
        return render_home(
            error="The uploaded file is empty. Please choose another image."
        )

    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return render_home(
            error="Invalid image. Please upload a valid image file."
        )

    height, width = image.shape[:2]

    face_detector.setInputSize((width, height))
    _, faces = face_detector.detect(image)

    face_count = 0 if faces is None else len(faces)

    # Save the successful image-processing record.
    with get_connection() as connection:
        connection.execute("""
            INSERT INTO detection_history (face_count, status)
            VALUES (?, ?)
        """, (face_count, "Success"))

    face_results = []

    if faces is not None:
        for face in faces:
            x, y, w, h = face[:4].astype(int)
            confidence = float(face[14])

            # Save each face detection record.
            face_record = save_detected_face(confidence)
            face_results.append(face_record)

            label = (
                f"{face_record['face_id']} | "
                f"{confidence * 100:.1f}%"
            )

            cv2.rectangle(
                image,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                image,
                label,
                (x, max(y - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    success, encoded_image = cv2.imencode(".jpg", image)

    if not success:
        return render_home(
            error="Could not process the image."
        )

    result_image = base64.b64encode(
        encoded_image
    ).decode("utf-8")

    return render_home(
        result_image=result_image,
        face_count=face_count,
        face_results=face_results
    )


@app.route("/export-history")
def export_history():
    """Export up to 10,000 recent image records as a CSV file."""
    records = get_detection_history(limit=10000)

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Record ID",
        "Timestamp (IST)",
        "Faces Detected",
        "Status"
    ])

    for record in records:
        writer.writerow([
            record["id"],
            format_ist_timestamp(record["timestamp"]),
            record["face_count"],
            record["status"]
        ])

    response = Response(
        output.getvalue(),
        mimetype="text/csv; charset=utf-8"
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=detection_history.csv"
    )

    return response


if __name__ == "__main__":
    app.run()
