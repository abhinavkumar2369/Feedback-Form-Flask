from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# ------- MySQL connection configuration ----------
MYSQL_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DATABASE', 'feedback_db'),
    'port': int(os.environ.get('MYSQL_PORT', 3306))
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**MYSQL_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_db_connection_without_db():
    """Create and return a database connection without specifying database (for initial setup)"""
    try:
        config_without_db = MYSQL_CONFIG.copy()
        config_without_db.pop('database', None)  # Remove database from config
        connection = mysql.connector.connect(**config_without_db)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

def init_database():
    """Initialize the database and create tables if they don't exist"""
    print("Initializing database...")
    
    try:
        # First, connect without specifying database to create it
        connection = get_db_connection_without_db()
        if not connection:
            print("❌ Failed to connect to MySQL server. Please check your connection settings.")
            return False
            
        cursor = connection.cursor()
        
        # Create database if it doesn't exist
        database_name = MYSQL_CONFIG['database']
        print(f"📁 Checking/Creating database: {database_name}")
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
        print(f"✅ Database '{database_name}' is ready!")
        
        # Switch to the database
        cursor.execute(f"USE `{database_name}`")
        
        # Create feedback table if it doesn't exist
        table_name = "feedback"
        print(f"📋 Checking/Creating table: {table_name}")
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS feedback (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            subject VARCHAR(500),
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_timestamp (timestamp),
            INDEX idx_email (email)
        )
        """
        cursor.execute(create_table_query)
        
        # Verify table was created by checking its structure
        cursor.execute("DESCRIBE feedback")
        table_structure = cursor.fetchall()
        
        if table_structure:
            print(f"✅ Table 'feedback' is ready with {len(table_structure)} columns!")
            print("📊 Table structure:")
            for column in table_structure:
                print(f"   - {column[0]}: {column[1]}")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("🎉 Database initialization completed successfully!")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ MySQL Error during database initialization: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during database initialization: {e}")
        return False

def test_database_connection():
    """Test the database connection and verify everything is working"""
    print("🔍 Testing database connection...")
    
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # Test basic query
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()
            print(f"✅ Connected to database: {current_db[0]}")
            
            # Check if feedback table exists and count records
            cursor.execute("SHOW TABLES LIKE 'feedback'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.execute("SELECT COUNT(*) FROM feedback")
                record_count = cursor.fetchone()[0]
                print(f"📊 Feedback table contains {record_count} records")
            else:
                print("⚠️ Feedback table not found!")
            
            cursor.close()
            connection.close()
            return True
        else:
            print("❌ Failed to connect to database")
            return False
            
    except mysql.connector.Error as e:
        print(f"❌ Database connection test failed: {e}")
        return False

# Initialize database on startup
print("🚀 Starting Flask Feedback Application...")
print("=" * 50)

if init_database():
    if test_database_connection():

        pass
    print("=" * 50)
    print("🌐 Application ready! Available routes:")
    print("   📝 Main Form: http://localhost:5000/")
    print("   📊 View Feedback: http://localhost:5000/feedback")
    print("   🔧 Reinit DB: http://localhost:5000/admin/init-db")
    print("=" * 50)
else:
    print("❌ Database initialization failed! Please check your MySQL configuration.")
    print("💡 Make sure MySQL server is running and credentials in .env are correct.")
    print("=" * 50)

def create_sample_data():
    """Create sample feedback data for testing (optional)"""
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            # Check if table is empty
            cursor.execute("SELECT COUNT(*) FROM feedback")
            count = cursor.fetchone()[0]
            
            if count == 0:
                print("📝 Adding sample feedback data...")
                
                sample_data = [
                    ("John Doe", "john@example.com", "+1-555-0123", "Great Service", "I really enjoyed using your service. Keep up the good work!", datetime.now()),
                    ("Jane Smith", "jane@example.com", "", "Suggestion", "It would be great if you could add a dark mode feature.", datetime.now()),
                    ("Bob Johnson", "bob@example.com", "+1-555-0456", "Bug Report", "I found a small bug in the login system. Please fix it.", datetime.now())
                ]
                
                insert_query = """
                INSERT INTO feedback (name, email, phone, subject, message, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                
                cursor.executemany(insert_query, sample_data)
                connection.commit()
                print(f"✅ Added {len(sample_data)} sample feedback entries!")
            
            cursor.close()
            connection.close()
            
    except mysql.connector.Error as e:
        print(f"❌ Error creating sample data: {e}")

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
        
        # ------- Inserting data into MySQL -------
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            
            insert_query = """
            INSERT INTO feedback (name, email, phone, subject, message, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            values = (name, email, phone, subject, message, datetime.now())
            cursor.execute(insert_query, values)
            connection.commit()
            
            if cursor.rowcount > 0:
                cursor.close()
                connection.close()
                return render_template('response.html', name=name)
            else:
                cursor.close()
                connection.close()
                flash('Error submitting feedback. Please try again.', 'error')
                return redirect(url_for('index'))
        else:
            flash('Database connection error. Please try again.', 'error')
            return redirect(url_for('index'))
            
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error: {e}")
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/feedback')
def view_feedback():
    try:
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            
            # Fetch all feedback ordered by timestamp (newest first)
            cursor.execute("SELECT * FROM feedback ORDER BY timestamp DESC")
            feedbacks = cursor.fetchall()
            
            cursor.close()
            connection.close()
            
            return render_template('feedback_list.html', feedbacks=feedbacks)
        else:
            flash('Database connection error. Please try again later.', 'error')
            return redirect(url_for('index'))
            
    except mysql.connector.Error as e:
        print(f"Error retrieving feedback: {e}")
        flash('Error retrieving feedback. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/admin/init-db')
def reinit_database():
    """Admin route to reinitialize database (for development/testing)"""
    print("\n🔄 Manual database reinitialization requested...")
    
    if init_database():
        test_database_connection()
        return "<h2>✅ Database reinitialized successfully!</h2><p><a href='/'>Back to Form</a> | <a href='/feedback'>View Feedback</a></p>"
    else:
        return "<h2>❌ Database reinitialization failed!</h2><p>Check console for error details.</p><p><a href='/'>Back to Form</a></p>"

@app.route('/admin/sample-data')
def add_sample_data():
    """Admin route to add sample data (for development/testing)"""
    print("\n📝 Adding sample data...")
    create_sample_data()
    return "<h2>✅ Sample data added!</h2><p><a href='/feedback'>View Feedback</a> | <a href='/'>Back to Form</a></p>"

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, port=port)