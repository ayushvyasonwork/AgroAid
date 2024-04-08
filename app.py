
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from newscrape import scrape_news
from schemescrape import scrape_schemes
from mspscrape import fetch_crop_row  # Import the function to fetch crop row
from pygal_script import generate_semicircle_gauge_chart
from objDetection import perform_object_detection
import time
from datetime import datetime
import pandas as pd

app = Flask(__name__, instance_path=r'C:\Python311\Scripts\MyPython\Practicum_IV(AgroAid)')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            # Perform login operation, for now, just redirecting to dashboard
            return redirect(url_for('dashboard'))
        else:
            return "<h1>Invalid email or password</h1>"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "User already exists. Please login."
        else:
            # Create new user and add to database
            new_user = User(email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('signup.html')

# Assuming you have a function to fetch data from Firebase
def fetch_data_from_firebase():
    # Replace this with your logic to fetch data from Firebase
    # For example:
    data = {
        'temperature': 25,
        'humidity': 50,
        'rain_value': 1,
        'soil_moisture': 30
    }
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/fetch-news')
def fetch_news():
    news = scrape_news()
    return jsonify(news)

@app.route('/fetch-schemes')
def fetch_schemes():
    schemes = scrape_schemes()
    return jsonify(schemes)

@app.route('/fetch-msp', methods=['POST'])
def fetch_msp():
    data = request.json
    selected_crop = data.get('crop')
    if selected_crop:
        row = fetch_crop_row(selected_crop)
        if row:
            return jsonify({'row': str(row)})
        else:
            return jsonify({'error': 'Crop not found'}), 404
    else:
        return jsonify({'error': 'Crop not provided'}), 400

@app.route('/fetch-gauge')
def fetch_gauge():
    # Fetch data from Firebase
    data = fetch_data_from_firebase()
    chart_html = ""
    # Generate gauge chart for each parameter
    for key, value in data.items():
        chart_html += generate_suitable_chart(key, value)
    return chart_html

def generate_suitable_chart(key, value):
    # Generate suitable chart based on the parameter
    return generate_semicircle_gauge_chart(value)

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s', (request.path,))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error,))
    return render_template('500.html'), 500

@app.route('/execute-object-detection', methods=['POST'])
def execute_object_detection():
    perform_object_detection()
    return jsonify({'message': 'Object detection script executed successfully'})

if __name__ == '__main__':
     # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
