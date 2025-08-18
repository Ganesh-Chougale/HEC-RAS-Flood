# App\backend-flask-app\database.py
import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Load environment variables
load_dotenv()

# Initialize the database object without an app
db = SQLAlchemy()

def init_db(app: Flask):
    """
    Initializes the database connection with the Flask application.
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

# Define the database models
class AlertThreshold(db.Model):
    """
    Model for storing flood alert thresholds.
    """
    __tablename__ = 'alert_thresholds'
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)
    parameter = db.Column(db.String(50), nullable=False)
    threshold_value = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    def __repr__(self):
        return f'<AlertThreshold {self.location_name} - {self.parameter}>'

class AlertLog(db.Model):
    """
    Model for logging triggered alerts.
    """
    __tablename__ = 'alert_log'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    location_name = db.Column(db.String(100), nullable=False)
    parameter = db.Column(db.String(50), nullable=False)
    triggered_value = db.Column(db.Float, nullable=False)
    threshold_value = db.Column(db.Float, nullable=False)
    log_message = db.Column(db.Text, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<AlertLog {self.location_name} - {self.timestamp}>'