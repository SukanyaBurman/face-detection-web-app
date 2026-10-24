# Face Detection Studio

A web-based face detection application built with Python, Flask, OpenCV, and SQLite. The application detects faces in uploaded images, displays confidence scores, and maintains a history of detection activity.

## Features

- **Face Detection:** Detect faces in uploaded images using OpenCV's YuNet model.
- **Visual Results:** Display detected faces with bounding boxes and confidence scores.
- **Unique Face IDs:** Assign IDs to individual detection records.
- **Detection History:** Store image-processing and face-detection records in SQLite.
- **Dashboard Analytics:** Display image counts, detected faces, average confidence, and seven-day activity.
- **CSV Export:** Export detection history for further analysis.
- **Input Validation:** Validate supported image formats and reject invalid or oversized uploads.
- **Timestamp Formatting:** Display detection timestamps in Indian Standard Time (IST).


## Technologies Used

- Python
- Flask
- OpenCV
- NumPy
- SQLite
- HTML5 and CSS3
- YuNet Face Detection Model
- pytest

## Project Structure

```text
face-detection-web-app/
├── app.py
├── database.py
├── test_app.py
├── requirements.txt
├── face_detection_yunet_2023mar.onnx
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── .gitignore
└── README.md
```

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

Activate it in Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

Open your browser at:

http://127.0.0.1:5000/


## Usage

1. Open Face Detection Studio in your browser.
2. Upload a supported JPG, JPEG, PNG, or WEBP image.
3. Run face detection.
4. Review the annotated image and confidence scores.
5. View detection history and dashboard analytics.
6. Export the history as a CSV file.

## Testing

Run the automated tests:

```bash
python -m pytest -v
```

The project previously passed six automated tests in the development environment. Run the command above to verify the current version.

## Limitations

- The application detects faces; it does not identify individuals.
- Face IDs represent detection records and do not track the same person across images.
- Results depend on image quality, lighting, face size, and model limitations.
- The current version is designed for local execution.
- Detection history is stored in SQLite.

## Security and Privacy

- Avoid uploading sensitive images to a public demonstration.
- Review file validation and data handling before deployment.
- Disable Flask debug mode in production.
- Configure persistent storage if detection history must survive hosting restarts or redeployments.

## Model Attribution

This project uses the YuNet face detection model distributed through the OpenCV Zoo project.

Model documentation: [OpenCV Zoo — YuNet](https://github.com/opencv/opencv_zoo/tree/main/models/face_detection_yunet)

Review the model's applicable licence and attribution requirements before redistributing the model file. The model licence does not automatically determine the licence for this application's code.

## Future Improvements

- Add application screenshots and a live demo.
- Improve automated test coverage.
- Add pagination and search for detection history.
- Configure production hosting and persistent database storage.

## Author

**Sukanya Burman**

- GitHub: [@SukanyaBurman](https://github.com/SukanyaBurman)
- Repository: [Face Detection Studio](https://github.com/SukanyaBurman/face-detection-web-app)
