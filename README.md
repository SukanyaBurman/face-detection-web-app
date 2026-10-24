# Face Detection Studio

A web-based face detection application built with Python, Flask, OpenCV, and SQLite. The application detects faces in uploaded images, displays confidence scores, and maintains a history of detection activity.

## Features

- **Face Detection:** Detect faces in uploaded images using OpenCV's YuNet model.
- **Visual Results:** Display detected faces with bounding boxes and confidence scores.
- **Unique Face IDs:** Assign an ID to each detection record.
- **Detection History:** Store image-processing records in SQLite.
- **Dashboard Analytics:** Display image counts, detected faces, average confidence, and seven-day activity.
- **CSV Export:** Export detection history for further analysis.
- **Input Validation:** Validate supported image formats and reject oversized or invalid uploads.
- **Timestamp Formatting:** Display detection timestamps in Indian Standard Time (IST).

## Technologies Used

- Python
- Flask
- OpenCV
- NumPy
- SQLite
- HTML5
- CSS3
- YuNet Face Detection Model

## Project Structure

```text
face-detection-web-app/
├── app.py
├── database.py
├── test_app.py
├── face_detection_yunet_2023mar.onnx
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── .gitignore
└── README.md
```

## Requirements

- Python
- pip
- The YuNet ONNX model included in the project
- A modern web browser

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   ```

2. Enter the project directory:

   ```bash
   cd face-detection-web-app
   ```

3. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On Windows:

   ```bash
   .venv\Scripts\activate
   ```

4. Install the required packages:

   ```bash
   python -m pip install Flask opencv-python numpy pytest
   ```

5. Start the application:

   ```bash
   python app.py
   ```

6. Open the application in your browser:

   `http://127.0.0.1:5000/`

## Testing

Run the automated tests using:

```bash
python -m pytest -v
```

The project has six passing tests in the current development environment.

## Usage

1. Open Face Detection Studio in your browser.
2. Upload a supported JPG, JPEG, PNG, or WEBP image.
3. Run face detection.
4. Review the annotated image and confidence scores.
5. View detection history and dashboard analytics.
6. Export the history as a CSV file.

## Limitations

- The application detects faces; it does not identify individuals.
- Face IDs represent detection records and do not track the same person across images.
- Detection accuracy depends on image quality, lighting, face size, and model limitations.
- The application is currently designed to run locally.

## Future Improvements

- Add image previews before processing.
- Improve automated test coverage.
- Add pagination and search for detection history.
- Deploy the application to a hosting platform.

## License

Add a license after deciding how you want others to use and distribute this project.
