# App\backend-flask-app\app.py
import os
import tempfile
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

# Import the dss_parser and database modules
from dss_parser import read_dss_data
from database import db, init_db, AlertThreshold, AlertLog

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
# Initialize the database with the app
init_db(app)

# Enable CORS for the frontend's origin
CORS(app, origins=["http://localhost:3000"])

# Global variable to store the path of the last uploaded file
last_dss_file_path = None
# In a production environment, use a secure path and clean up old files
UPLOAD_FOLDER = os.path.join(tempfile.gettempdir(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# A simple route to test database connection
@app.route('/test-db')
def test_db_connection():
    try:
        # Try to count the number of rows in a table
        count = db.session.query(AlertThreshold).count()
        return jsonify({"message": f"Successfully connected to the database. Found {count} alert thresholds."}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to connect to the database: {str(e)}"}), 500

@app.route('/')
def hello_world():
    return 'Hello, World! This is your Flask Backend.'

@app.route('/api/upload-dss', methods=['POST'])
def upload_dss():
    """
    Handles DSS file upload, saves it, and extracts data.
    """
    global last_dss_file_path
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            last_dss_file_path = file_path
            
            dss_path = "/Panchganga/Rajaram Bridge/FLOW/01Jan2021/1Day/Observed Discharge/"
            extracted_data = read_dss_data(file_path, dss_path)
            
            if not extracted_data:
                return jsonify({'error': 'Failed to extract data from the DSS file. Check the file path and internal data path.'}), 500

            # ----------------------------------------------------
            # Future Integration Point: Alert Logic
            # ----------------------------------------------------
            # Here, after extracting data, you would loop through it,
            # retrieve alert thresholds from AlertThreshold table,
            # and compare values to decide if an alert should be logged.
            # Example: 
            # if any(d['value'] > threshold_from_db for d in extracted_data):
            #    # Log an alert to the AlertLog table
            #    pass
            # ----------------------------------------------------

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
        dss_path = "/Panchganga/Rajaram Bridge/FLOW/01Jan2021/1Day/Observed Discharge/"
        extracted_data = read_dss_data(last_dss_file_path, dss_path)

        if not extracted_data:
            return jsonify({'error': 'Failed to re-process data for download.'}), 500
        
        df = pd.DataFrame(extracted_data)
        csv_string = df.to_csv(index=False)
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

@app.route('/api/trigger-placeholder-alert', methods=['POST'])
def trigger_placeholder_alert():
    """
    A placeholder endpoint to simulate an alert trigger.
    """
    try:
        # A hardcoded alert for a specific location
        new_alert = AlertLog(
            location_name="Rajaram Bridge",
            parameter="FLOW",
            triggered_value=99999.99,  # A dummy value to simulate an exceedance
            threshold_value=50000.0,
            log_message="Simulated alert triggered for testing purposes."
        )
        db.session.add(new_alert)
        db.session.commit()
        
        return jsonify({
            'message': 'Placeholder alert successfully logged to the database!'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to trigger placeholder alert: {str(e)}'}), 500

if __name__ == '__main__':
    # Add a context manager to the app for database operations outside of requests
    with app.app_context():
        # This will create the tables defined in the models if they don't exist
        db.create_all()
        # You can also add some initial data here for testing
        if not AlertThreshold.query.first():
            initial_threshold = AlertThreshold(
                location_name="Rajaram Bridge",
                parameter="FLOW",
                threshold_value=50000.0, # A sample threshold in CMS
                is_active=True
            )
            db.session.add(initial_threshold)
            db.session.commit()
            print("Initial alert threshold added to the database.")
        
    app.run(debug=True, port=5000)