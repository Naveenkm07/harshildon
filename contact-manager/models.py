from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Contact(db.Model):
    """Contact model for storing contact information"""
    
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False, index=True)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    address = db.Column(db.Text, nullable=True)
    company = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Contact {self.full_name}>'
    
    def to_dict(self):
        """Convert contact to dictionary"""
        return {
            'id': self.id,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'email': self.email,
            'address': self.address,
            'company': self.company,
            'notes': self.notes,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @staticmethod
    def search(query):
        """Search contacts by name, phone, or email"""
        search_pattern = f'%{query}%'
        return Contact.query.filter(
            db.or_(
                Contact.full_name.ilike(search_pattern),
                Contact.phone_number.like(search_pattern),
                Contact.email.ilike(search_pattern)
            )
        ).order_by(Contact.full_name).all()
