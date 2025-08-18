# app.py
import os
import tempfile
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

# Import the dss_parser module
from dss_parser import read_dss_data

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Enable CORS for the frontend's origin
CORS(app, origins=["http://localhost:3000"])

# Global variable to store the path of the last uploaded file
# In a production environment, you would use a database or more robust caching
last_dss_file_path = None
# In a production environment, use a secure path and clean up old files
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def hello_world():
    return 'Hello, World! This is your Flask Backend.'

@app.route('/api/upload-dss', methods=['POST'])
def upload_dss():
    """
    Handles DSS file upload, saves it, and extracts data.
    """
    global last_dss_file_path
    
    # 1. Receive the uploaded DSS file
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            # 2. Securely save the file temporarily
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            last_dss_file_path = file_path
            
            # This is a hardcoded path for the test file.
            path_message = "# In a real-world scenario, you might have the user select this."
            dss_path = "/Panchganga/Rajaram Bridge/FLOW/01Jan2021/1Day/Observed Discharge/"

            # 3. Call your dss_parser module to extract data
            extracted_data = read_dss_data(file_path, dss_path)
            
            if not extracted_data:
                return jsonify({'error': 'Failed to extract data from the DSS file. Check the file path and internal data path.'}), 500
            
            # 4. Return the extracted data as JSON
            return jsonify({
                'message': 'File uploaded and data extracted successfully!',
                'data': extracted_data
            }), 200
        
        except Exception as e:
            return jsonify({'error': f'An internal server error occurred: {str(e)}'}), 500

@app.route('/api/download-csv', methods=['GET'])
def download_csv():
    """
    Converts extracted data to CSV and provides it for download.
    """
    global last_dss_file_path

    if not last_dss_file_path or not os.path.exists(last_dss_file_path):
        return jsonify({'error': 'No DSS file has been processed yet.'}), 404

    try:
        # A. Re-process the file to get the latest data
        dss_path = "/Panchganga/Rajaram Bridge/FLOW/01Jan2021/1Day/Observed Discharge/"
        extracted_data = read_dss_data(last_dss_file_path, dss_path)

        if not extracted_data:
            return jsonify({'error': 'Failed to re-process data for download.'}), 500
        
        df = pd.DataFrame(extracted_data)
        
        # Convert DataFrame to a CSV string
        csv_string = df.to_csv(index=False)
        
        # B. Return the CSV file with correct headers
        output_file_path = os.path.join(tempfile.gettempdir(), 'discharge_data.csv')
        with open(output_file_path, 'w', newline='') as f:
            f.write(csv_string)
            
        return send_file(
            output_file_path,
            mimetype='text/csv',
            as_attachment=True,
            download_name='discharge_data.csv'
        )

    except Exception as e:
        return jsonify({'error': f'An internal server error occurred: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)