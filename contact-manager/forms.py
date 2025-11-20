import re
from email_validator import validate_email, EmailNotValidError

class ContactForm:
    """Form validation for contact data"""
    
    def __init__(self, data):
        self.data = data
        self.errors = {}
    
    def validate(self):
        """Validate all contact fields"""
        self._validate_full_name()
        self._validate_phone_number()
        self._validate_email()
        # Optional fields don't need validation
        return len(self.errors) == 0
    
    def _validate_full_name(self):
        """Validate full name"""
        name = self.data.get('full_name', '').strip()
        if not name:
            self.errors['full_name'] = 'Full name is required.'
        elif len(name) < 2:
            self.errors['full_name'] = 'Full name must be at least 2 characters.'
        elif len(name) > 100:
            self.errors['full_name'] = 'Full name must not exceed 100 characters.'
    
    def _validate_phone_number(self):
        """Validate phone number"""
        phone = self.data.get('phone_number', '').strip()
        if not phone:
            self.errors['phone_number'] = 'Phone number is required.'
        elif len(phone) < 10:
            self.errors['phone_number'] = 'Phone number must be at least 10 digits.'
        elif len(phone) > 20:
            self.errors['phone_number'] = 'Phone number must not exceed 20 characters.'
        # Check if it contains at least some digits
        elif not re.search(r'\d', phone):
            self.errors['phone_number'] = 'Phone number must contain digits.'
    
    def _validate_email(self):
        """Validate email format"""
        email = self.data.get('email', '').strip()
        if not email:
            self.errors['email'] = 'Email is required.'
        else:
            try:
                # Validate email format
                validate_email(email)
            except EmailNotValidError as e:
                self.errors['email'] = f'Invalid email format: {str(e)}'
    
    def get_cleaned_data(self):
        """Return cleaned and validated data"""
        return {
            'full_name': self.data.get('full_name', '').strip(),
            'phone_number': self.data.get('phone_number', '').strip(),
            'email': self.data.get('email', '').strip().lower(),
            'address': self.data.get('address', '').strip() or None,
            'company': self.data.get('company', '').strip() or None,
            'notes': self.data.get('notes', '').strip() or None
        }
