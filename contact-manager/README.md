# Contact Manager with Database Support

A fully functional web-based contact management system built with Flask and SQLite. Features include complete CRUD operations, search functionality, CSV import/export, and a responsive user interface.

## Features

- ✅ **Full CRUD Operations** - Create, Read, Update, Delete contacts
- 🔍 **Search & Filter** - Search by name, phone, or email
- 💾 **Database Persistence** - SQLite with easy MySQL migration path
- 📊 **CSV Import/Export** - Bulk manage contacts
- 📱 **Responsive Design** - Works on desktop and mobile
- 🔒 **Input Validation** - Server-side validation for all fields
- 📝 **Logging** - Complete activity logging
- ⚡ **Pagination** - Handle large contact lists efficiently

## Technology Stack

- **Backend**: Flask 3.0
- **Database**: SQLite (via SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **ORM**: Flask-SQLAlchemy

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone or Download

Download all the files into a directory called `contact-manager`.

### Step 2: Create Virtual Environment (Recommended)

Creating a virtual environment is recommended to isolate project dependencies:

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Navigate to the project directory and install required packages:

```bash
cd contact-manager
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- email-validator 2.1.0
- python-dateutil 2.8.2

### Step 4: Configure the Application

The application uses a `config.py` file for configuration. By default, it uses SQLite database. You can modify settings in `config.py` if needed:

- **Database**: SQLite (default) - creates `contacts.db` in the project directory
- **Secret Key**: Change the `SECRET_KEY` in production
- **Logging**: Logs are stored in `logs/app.log`

### Step 5: Initialize the Database

The database will be automatically created when you first run the application. No manual setup required!

### Step 6: Run the Application

Start the Flask development server:

```bash
python app.py
```

The application will start on `http://localhost:4000` (or `http://0.0.0.0:4000`).

### Step 7: Access the Application

Open your web browser and navigate to:
```
http://localhost:4000
```

## Usage

### Adding Contacts

1. Click "Add Contact" in the navigation menu
2. Fill in the required fields (Full Name, Phone Number, Email)
3. Optionally add Address, Company, and Notes
4. Click "Save Contact"

### Searching Contacts

1. Go to the Contacts page
2. Use the search bar to search by name, phone, or email
3. Results are displayed in real-time

### Importing Contacts

1. Navigate to "Import/Export" page
2. Prepare a CSV file with the following columns:
   - `full_name` (required)
   - `phone_number` (required)
   - `email` (required)
   - `address` (optional)
   - `company` (optional)
   - `notes` (optional)
3. Click "Choose File" and select your CSV
4. Click "Import Contacts"

### Exporting Contacts

1. Navigate to "Import/Export" page
2. Click "Export to CSV"
3. All contacts will be downloaded as a CSV file

## Project Structure

```
contact-manager/
├── app.py                      # Application entry point and routes
├── models.py                   # Database models (Contact)
├── forms.py                    # Form validation logic
├── database.py                 # Database initialization functions
├── utils.py                    # Helper functions (CSV import/export)
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── contacts.db                 # SQLite database (created on first run)
├── logs/
│   └── app.log                 # Application logs
├── static/
│   ├── css/
│   │   └── styles.css          # Custom styles
│   └── js/
│       └── scripts.js          # JavaScript for interactivity
└── templates/
    ├── base.html               # Base template
    ├── index.html              # Home page
    ├── contacts_list.html      # List all contacts
    ├── contact_form.html       # Add/Edit contact form
    ├── contact_detail.html     # View single contact
    └── import_export.html      # Import/Export page
```

## CSV Import Format

When importing contacts from CSV, ensure your file has the following columns:

**Required columns:**
- `full_name` - Contact's full name
- `phone_number` - Phone number (at least 10 digits)
- `email` - Valid email address

**Optional columns:**
- `address` - Street address
- `company` - Company name
- `notes` - Additional notes

**Example CSV:**
```csv
full_name,phone_number,email,address,company,notes
John Doe,1234567890,john@example.com,123 Main St,Acme Corp,Important client
Jane Smith,0987654321,jane@example.com,456 Oak Ave,,Friend
```

## Configuration

### Environment Variables

You can configure the application using environment variables:

- `DATABASE_URL` - Database connection string (defaults to SQLite)
- `SECRET_KEY` - Secret key for Flask sessions (change in production!)

### Database Configuration

**SQLite (Default):**
The application uses SQLite by default, which creates a `contacts.db` file automatically.

**MySQL (Optional):**
To use MySQL, update `config.py`:
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/contact_manager'
```
Don't forget to install the MySQL driver:
```bash
pip install pymysql
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   - Change the port in `app.py`: `app.run(debug=True, host='0.0.0.0', port=5001)`

2. **Database errors:**
   - Delete `contacts.db` and restart the application to recreate the database

3. **Import errors:**
   - Ensure CSV file has correct column names
   - Check that required fields are not empty
   - Verify email format is valid

4. **Module not found errors:**
   - Make sure virtual environment is activated
   - Run `pip install -r requirements.txt` again

## Development

### Running in Development Mode

The application runs in debug mode by default. To disable:
- Set `DEBUG = False` in `config.py` or use environment variable

### Logging

Application logs are stored in `logs/app.log` with rotation (10MB max, 10 backups).

### Database Reset

To reset the database (use with caution):
```python
from database import reset_db
reset_db(app)
```

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## Support

For issues or questions, please check the logs in `logs/app.log` for detailed error messages.
