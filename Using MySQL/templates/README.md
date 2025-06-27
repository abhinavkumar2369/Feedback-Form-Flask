# Flask Feedback Form with MySQL

A simple web application built with Flask and MySQL for collecting and managing user feedback.

## Features

- Submit feedback through a responsive web form
- Store feedback data in MySQL database
- View all submitted feedback in an admin panel
- Environment variable configuration
- Form validation and error handling
- Modern, responsive web interface
- Automatic database and table creation

## Prerequisites

- Python 3.7+
- MySQL Server (local installation or remote connection)
- pip (Python package manager)

## Installation

1. Clone or download the project
2. Navigate to the project directory:
   ```bash
   cd "c:\Users\Abhinav Kumar\Desktop\Feedback-Form-Flask\Using MySQL"
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up MySQL:
   - Install MySQL Server locally or use a cloud service
   - Ensure MySQL Server is running
   - Create a database user (or use root)

## Configuration

1. Update the `.env` file with your MySQL configuration:

```env
SECRET_KEY=your_secret_key_here
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=feedback_db
MYSQL_PORT=3306
FLASK_DEBUG=True
PORT=5000
```

## Environment Variables

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `SECRET_KEY` | Flask secret key for session management | `default_secret_key` |
| `MYSQL_HOST` | MySQL server hostname | `localhost` |
| `MYSQL_USER` | MySQL username | `root` |
| `MYSQL_PASSWORD` | MySQL password | (empty) |
| `MYSQL_DATABASE` | MySQL database name | `feedback_db` |
| `MYSQL_PORT` | MySQL port number | `3306` |
| `FLASK_DEBUG` | Enable/disable debug mode | `True` |
| `PORT` | Port number for the Flask app | `5000` |

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Fill out the feedback form and submit
4. View all feedback at:
   ```
   http://localhost:5000/feedback
   ```

## Project Structure

```
Using MySQL/
├── app.py                 # Main Flask application
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/               # Static files
│   └── style.css         # CSS styles
└── templates/            # HTML templates
    ├── index.html        # Feedback form
    ├── response.html     # Submission confirmation
    └── feedback_list.html # View all feedback
```

## API Endpoints

- `GET /` - Display feedback form
- `POST /submit` - Submit feedback data
- `GET /feedback` - View all submitted feedback

## Database Schema

The application automatically creates a `feedback` table with the following structure:

```sql
CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    subject VARCHAR(500),
    message TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Key Features

### Automatic Database Setup
- Creates database if it doesn't exist
- Creates table automatically on first run
- No manual SQL setup required

### Form Validation
- Client-side HTML5 validation
- Server-side validation for required fields
- User-friendly error messages

### Responsive Design
- Mobile-first responsive layout
- Modern UI with gradient backgrounds
- Optimized for all screen sizes

### Error Handling
- Comprehensive error handling for database operations
- User-friendly error messages
- Graceful failure handling

## Security Notes

- Always use a strong `SECRET_KEY` in production
- Never commit the `.env` file to version control
- Use environment-specific configuration for different deployments
- Consider using SSL/TLS for production MySQL connections
- Implement proper user authentication for the admin view

## Troubleshooting

1. **MySQL Connection Error**: 
   - Ensure MySQL Server is running
   - Verify credentials in `.env` file
   - Check if the specified database exists (app will create it if not)

2. **Module Not Found**: 
   - Install required packages: `pip install -r requirements.txt`

3. **Port Already in Use**: 
   - Change the PORT variable in `.env`
   - Or kill the process using the port: `netstat -ano | findstr :5000`

4. **Permission Denied (MySQL)**: 
   - Ensure the MySQL user has CREATE and INSERT privileges
   - Grant necessary permissions: `GRANT ALL PRIVILEGES ON feedback_db.* TO 'username'@'localhost';`

## Differences from MongoDB Version

- Uses MySQL instead of MongoDB for data storage
- Relational database structure with defined schema
- Automatic database and table creation
- SQL queries instead of document operations
- Additional MySQL-specific error handling

## Production Deployment

For production deployment:

1. Set `FLASK_DEBUG=False` in `.env`
2. Use a production WSGI server like Gunicorn
3. Set up SSL/TLS for database connections
4. Use environment variables instead of `.env` file
5. Implement proper authentication for admin routes
6. Set up database backups

## License

This project is for educational purposes.
