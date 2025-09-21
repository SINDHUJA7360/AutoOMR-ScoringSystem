
AutoOMR Scoring System

Automated Optical Mark Recognition (OMR) for Efficient Exam Evaluation

> "Auto-score exams in minutes, not days."



The AutoOMR Scoring System is designed to automate the evaluation of OMR sheets using Python, HTML, and Jupyter Notebooks. It processes scanned or photographed OMR sheets, detects marked answers, compares them with an answer key, and generates detailed results with visual feedback, eliminating manual evaluation errors and saving time.

Features

Automated Evaluation: Detects responses and calculates marks automatically.

Visual Feedback: Highlights correct answers in green, wrong answers in red, and unmarked correct options in yellow.

Detailed Reporting: Displays total marks, percentage, and grade on the input sheet.

Web Interface: Simple frontend to upload sheets and view results.

Data Storage: Results can be saved in a local database (results.db).


Technologies Used

Python – Core backend logic for image processing and evaluation

OpenCV – Image preprocessing, edge detection, contour detection, and perspective transforms

NumPy – For numerical computations and matrix operations

Jupyter Notebooks – For testing, analysis, and development workflow

HTML/CSS/Frontend – For creating the web interface

SQLite – To store evaluation results

How It Works

1. Image Preprocessing – Converts input OMR images to grayscale and applies Gaussian blur to reduce noise.


2. Edge & Contour Detection – Detects bubbles using Canny edge detection and finds rectangular contours.


3. Perspective Transform – Converts sheets into a bird’s-eye view for consistent detection.


4. Bubble Detection & Evaluation – Measures pixel intensity to identify marked answers and compares them with the answer key.


5. Result Annotation – Annotates the original sheet with color-coded results, marks, and grade.




---

Installation

1. Clone the repository:

git clone https://github.com/SINDHUJA7360/AutoOMR-ScoringSystem.git
cd AutoOMR-ScoringSystem

2. Install dependencies: pip install -r requirements.txt

3. Run the app (Streamlit or Jupyter Notebook depending on your workflow): streamlit run app.py

Sample Output

(Include screenshots of evaluated OMR sheets showing color-coded answers, total marks, percentage, and grade)


Future Enhancements

Support Multiple Sheet Formats – Handle different layouts and structures.
Batch Processing – Evaluate multiple sheets at once.
AI-based Detection – Improve accuracy for faint or ambiguous markings.
Export Results – Export evaluation reports as CSV, PDF, or Excel.






