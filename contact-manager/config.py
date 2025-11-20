import os

class Config:
    """Application configuration"""
    
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Database configuration
    # SQLite by default - easily switchable to MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(BASE_DIR, "contacts.db")}'
    
    # For MySQL, use:
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/contact_manager'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret key for sessions and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Pagination
    CONTACTS_PER_PAGE = 10
    
    # Logging
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')
    LOG_LEVEL = 'INFO'
    
    # Upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'csv'}
