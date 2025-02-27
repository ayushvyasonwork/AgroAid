
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from newscrape import scrape_news
from schemescrape import scrape_schemes
# from mspscrape import fetch_crop_row  # Import the function to fetch crop row
import time
import subprocess
from datetime import datetime
import pandas as pd
import openai
import os
import secrets

# Absolute path to your 'instance' directory
instance_path = os.path.abspath(r'C:\Python311\Scripts\MyPython\Practicum_IV(AgroAid)')

app = Flask(__name__, instance_path=instance_path)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Generate a secure random key
secret_key = secrets.token_hex(16)  # Generate a 32-character hexadecimal string
app.config['SECRET_KEY'] = secret_key
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
            session['logged_in'] = True  # Set session variable upon successful login
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

@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Clear the session upon logout
    return redirect(url_for('login'))

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

@app.route('/get_crop', methods=['POST'])
def get_crop():
    try:
        # Extract data from the request
        data = request.json.get("data")
        
        # Modify the path to main.py as needed
        main_script_path = os.path.join(os.path.dirname(__file__), 'main.py')  
        
        # Pass the data to the main.py script and capture the response
        response = subprocess.run(['python', main_script_path, data], capture_output=True, text=True)
        response_text = response.stdout.strip()  # Get the response from the stdout
        print("Response:", response_text)  # Print the response to the console
        
        return jsonify(response=response_text)
    except Exception as e:
        return jsonify(error=str(e))
    
@app.route('/run-script')
def run_script():
    script_path = request.args.get('script')
    if script_path:
        try:
            # Execute the Python script
            subprocess.run(['python', script_path])
            return jsonify({'message': 'Script executed successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Script path not provided'}), 400
 
@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s', (request.path,))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error,))
    return render_template('500.html'), 500

if __name__ == '__main__':
     # Create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
