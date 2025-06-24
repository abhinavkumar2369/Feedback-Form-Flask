from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# ------- MongoDB connection ----------
try:
    # Use environment variables for MongoDB configuration
    mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
    db_name = os.environ.get('DB_NAME', 'feedback_db')
    collection_name = os.environ.get('COLLECTION_NAME', 'feedback')
    
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_feedback():
    try:
        # ---------- FORM DATA ----------
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # ---------- Validation ----------
        if not all([name, email, message]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))
        
        # -------- Schema --------
        feedback_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'subject': subject,
            'message': message,
            'timestamp': datetime.now()
        }
        
        # ------- Inserting data into MongoDB -------
        result = collection.insert_one(feedback_data)
        
        if result.inserted_id:
            return render_template('response.html', name=name)
        else:
            flash('Error submitting feedback. Please try again.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))


@app.route('/feedback')
def view_feedback():
    try:
        feedbacks = list(collection.find().sort('timestamp', -1))
        return render_template('feedback_list.html', feedbacks=feedbacks)
    except Exception as e:
        print(f"Error retrieving feedback: {e}")
        return "Error retrieving feedback"


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, port=port)
