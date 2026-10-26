# Face Detection Studio

**Live Demo:** https://face-detection-web-app-pid7.onrender.com


A web-based face detection application built with Python, Flask, OpenCV, and SQLite. Face Detection Studio detects faces in uploaded images, displays bounding boxes and confidence scores, and maintains a history of detection activity through an interactive dashboard.

## Features

- **Face Detection:** Detect faces in uploaded images using OpenCV's YuNet model.
- **Visual Results:** Display detected faces with bounding boxes and confidence scores.
- **Unique Face IDs:** Assign unique IDs to individual face detection records.
- **Detection History:** Store image-processing and face-detection records in SQLite.
- **Dashboard Analytics:** Display total images processed, detected faces, average confidence, and seven-day activity.
- **CSV Export:** Export detection history for further analysis.
- **Input Validation:** Validate supported image formats and reject invalid or oversized uploads.
- **Timestamp Formatting:** Display detection timestamps in Indian Standard Time (IST).
- **Automated Testing:** Use pytest to run automated application tests.

## Technologies Used

- Python
- Flask
- OpenCV
- NumPy
- SQLite
- HTML5
- CSS3
- YuNet Face Detection Model
- pytest
- Gunicorn (production deployment)

## Project Structure

```text
face-detection-web-app/
|-- app.py
|-- database.py
|-- test_app.py
|-- requirements.txt
|-- face_detection_yunet_2023mar.onnx
|-- templates/
|   `-- index.html
|-- static/
|   `-- style.css
|-- .gitignore
`-- README.md
```

The SQLite database file, `detection_history.db`, is created locally when the application initializes the database.

## Requirements

- Python 3
- pip
- A modern web browser
- The YuNet ONNX model included in the project

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/SukanyaBurman/face-detection-web-app.git
cd face-detection-web-app
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application locally

```bash
python app.py
```

Open the following address in your browser:

http://127.0.0.1:5000/

## Usage

1. Open Face Detection Studio in your browser.
2. Upload a supported JPG, JPEG, PNG, or WEBP image.
3. Run face detection.
4. Review the annotated image and confidence scores.
5. View detection history and dashboard analytics.
6. Export detection history as a CSV file.

## Testing

Run the automated tests using:

```bash
python -m pytest -v
```

The project previously passed six automated tests in the development environment. Run the command above to verify the current version.

## Limitations

- The application detects faces; it does not identify individuals.
- Face IDs represent individual detection records and do not track the same person across different images.
- Detection results depend on image quality, lighting, face size, and model limitations.
- The application uses SQLite for detection history.
- The local version is intended for development and demonstration purposes.

## Security and Privacy

- Validate uploaded files before processing them.
- Avoid uploading sensitive or confidential images to a public demonstration.
- Disable Flask debug mode in production.
- Configure appropriate storage and data-retention policies before public deployment.
- Use persistent storage if detection history must survive hosting restarts or redeployments.
- Do not assume that files stored on a free hosting service will persist indefinitely.

## Model Attribution

This project uses the YuNet face detection model distributed through OpenCV Zoo.

- **Model file:** `face_detection_yunet_2023mar.onnx`
- **Model source:** [OpenCV Zoo ΓÇö YuNet](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)

Refer to the model directory's licence and attribution requirements when using or redistributing the model.

## Future Improvements

- Add application screenshots and a live demo.
- Improve automated test coverage.
- Add pagination and search for detection history.
- Improve deployment configuration and persistent database storage.
- Enhance the dashboard with additional analytics.

## Author

**Sukanya Burman**

GitHub: [SukanyaBurman](https://github.com/SukanyaBurman)

Project Repository: [Face Detection Studio](https://github.com/SukanyaBurman/face-detection-web-app)
