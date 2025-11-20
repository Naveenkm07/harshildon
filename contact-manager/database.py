import logging
from models import db

logger = logging.getLogger(__name__)

def init_db(app):
    """Initialize database"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            logger.info('Database initialized successfully')
        except Exception as e:
            logger.error(f'Error initializing database: {str(e)}')
            raise

def reset_db(app):
    """Reset database (use with caution!)"""
    with app.app_context():
        try:
            db.drop_all()
            db.create_all()
            logger.warning('Database reset completed')
        except Exception as e:
            logger.error(f'Error resetting database: {str(e)}')
            raise
