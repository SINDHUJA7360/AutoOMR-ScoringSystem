import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from imutils import contours
import os

# You can now delete the find_sheet function entirely
# as we will no longer use it.

def process_omr_sheet(image, answer_key):
    # This is the updated code
    
    # Create a debug folder to save images
    debug_dir = 'debug_output'
    if not os.path.exists(debug_dir):
        os.makedirs(debug_dir)

    # Convert the original image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(debug_dir, '1_grayscale.png'), gray_image)
    
    # Apply Adaptive Thresholding
    thresh = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    cv2.imwrite(os.path.join(debug_dir, '2_thresh.png'), thresh)
    
    # Find contours
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    question_cnts = []
    
    # Loop over the contours and find the answer bubbles
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if w >= 15 and h >= 15 and ar >= 0.9 and ar <= 1.1:
            question_cnts.append(c)
            
    # Add this new check:
    if len(question_cnts) == 0:
        print("Error: No contours found that match OMR bubbles.")
        return {"total_score": 0, "subject_scores": {"Python": 0, "Data Analytics": 0, "MySQL": 0, "Power BI": 0, "Adv Stats": 0}}
    
    question_cnts = contours.sort_contours(question_cnts, method="top-to-bottom")[0]
    
    # Draw contours on a new image for visual debugging
    output_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(output_image, question_cnts, -1, (0, 255, 0), 2)
    cv2.imwrite(os.path.join(debug_dir, '3_contours.png'), output_image)
    
    results = {}
    subject_scores = {}
    total_correct = 0

    subject_ranges = {
        "Python": range(0, 20),
        "Data Analytics": range(20, 40),
        "MySQL": range(40, 60),
        "Power BI": range(60, 80),
        "Adv Stats": range(80, 100),
    }

    for subject, q_range in subject_ranges.items():
        subject_score = 0
        for (q_idx, i) in enumerate(np.arange(q_range.start, q_range.stop)):
            if i * 5 + 5 > len(question_cnts):
                continue
            cnts_for_q = contours.sort_contours(question_cnts[i*5:(i*5)+5])[0]
            bubbled = None

            for (j, c) in enumerate(cnts_for_q):
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                total = cv2.countNonZero(mask)
                
                if bubbled is None or total > bubbled[0]:
                    bubbled = (total, j)
            
            if bubbled and bubbled[1] == answer_key[i]:
                subject_score += 1
                total_correct += 1
        subject_scores[subject] = subject_score
    
    results["total_score"] = total_correct
    results["subject_scores"] = subject_scores
    return results