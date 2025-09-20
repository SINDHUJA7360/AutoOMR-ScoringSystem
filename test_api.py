import requests
import os

api_url = "http://127.0.0.1:5000/api/evaluate_omr"
    
# This is a direct relative path from your my_omr_project folder to the image
file_path = os.path.join('..', 'Theme 1 - Sample Data', 'Set A', 'Img5.jpeg')

# Check if the file path is correct
if not os.path.exists(file_path):
    print("Error: The file path does not exist.")
    print(f"Trying to find file at: {os.path.abspath(file_path)}")
else:
    try:
        with open(file_path, 'rb') as f:
            files = {'omr_sheet': f}
            response = requests.post(api_url, files=files)
            print("Status Code:", response.status_code)
            print("Response Body:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")