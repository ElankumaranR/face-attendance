Face Attendance System

This project is a facial recognition-based attendance system built using Python and Flask. The system uses a camera to capture and recognize faces, marking attendance automatically.
Features

    Real-time face detection and recognition
    Attendance marking and logging
    Web interface for managing attendance records
    Easy-to-use configuration and setup

Prerequisites

    Python 3.6 or higher
    Flask
    OpenCV
    NumPy
    Face recognition library

Installation

    Clone the repository:

    bash

git clone https://github.com/ElankumaranR/face-attendance.git
cd face-attendance

Create a virtual environment:

bash

python3 -m venv venv
source venv/bin/activate   # On Windows, use `venv\Scripts\activate`

Install dependencies:

bash

    pip install -r requirements.txt

    Download the pre-trained face detection model:

    Download the required models and place them in the appropriate directories. (You may provide specific instructions if needed.)

Usage

    Run the Flask server:

    bash

    python app.py

    Access the web interface:

    Open your browser and go to http://127.0.0.1:5000/.

    Capture and Register Faces:

    Use the web interface to capture and register faces for attendance.

    Mark Attendance:

    The system will automatically mark attendance based on facial recognition.

Directory Structure

php

face-attendance/
│
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
├── static/                  # Static files (CSS, JavaScript, images)
├── templates/               # HTML templates
├── models/                  # Pre-trained models and related files
├── utils/                   # Utility functions
└── README.md                # Project README file



    


