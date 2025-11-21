import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from datetime import datetime
import io

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import Config
from models import db, Contact
from forms import ContactForm
from database import init_db
from utils import export_contacts_to_csv, import_contacts_from_csv, allowed_file

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler(
    app.config['LOG_FILE'],
    maxBytes=10240000,  # 10MB
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Contact Manager startup')

# Initialize database tables
with app.app_context():
    init_db(app)

# Routes

@app.route('/')
def index():
    """Home page"""
    try:
        total_contacts = Contact.query.count()
        return render_template('index.html', total_contacts=total_contacts)
    except Exception as e:
        app.logger.error(f'Error loading home page: {str(e)}')
        flash('An error occurred while loading the page.', 'error')
        return render_template('index.html', total_contacts=0)

@app.route('/contacts')
def contacts_list():
    """List all contacts with search and pagination"""
    try:
        # Get search query
        search_query = request.args.get('search', '').strip()
        page = request.args.get('page', 1, type=int)
        
        # Base query
        if search_query:
            contacts = Contact.search(search_query)
            # Manual pagination for search results
            total = len(contacts)
            start = (page - 1) * app.config['CONTACTS_PER_PAGE']
            end = start + app.config['CONTACTS_PER_PAGE']
            contacts_page = contacts[start:end]
            
            # Create a mock pagination object
            class MockPagination:
                def __init__(self, items, page, per_page, total):
                    self.items = items
                    self.page = page
                    self.per_page = per_page
                    self.total = total
                    self.pages = (total + per_page - 1) // per_page
                    self.has_prev = page > 1
                    self.has_next = page < self.pages
                    self.prev_num = page - 1 if self.has_prev else None
                    self.next_num = page + 1 if self.has_next else None
            
            pagination = MockPagination(contacts_page, page, app.config['CONTACTS_PER_PAGE'], total)
        else:
            # Use SQLAlchemy pagination
            pagination = Contact.query.order_by(Contact.full_name).paginate(
                page=page,
                per_page=app.config['CONTACTS_PER_PAGE'],
                error_out=False
            )
        
        return render_template(
            'contacts_list.html',
            contacts=pagination.items,
            pagination=pagination,
            search_query=search_query
        )
    except Exception as e:
        app.logger.error(f'Error loading contacts list: {str(e)}')
        flash('An error occurred while loading contacts.', 'error')
        return render_template('contacts_list.html', contacts=[], pagination=None)

@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    """Add new contact"""
    if request.method == 'POST':
        try:
            # Validate form
            form = ContactForm(request.form)
            
            if not form.validate():
                for field, error in form.errors.items():
                    flash(f'{field.replace("_", " ").title()}: {error}', 'error')
                return render_template('contact_form.html', contact=None, form_data=request.form)
            
            # Create new contact
            cleaned_data = form.get_cleaned_data()
            contact = Contact(**cleaned_data)
            
            db.session.add(contact)
            db.session.commit()
            
            app.logger.info(f'Contact created: {contact.full_name} (ID: {contact.id})')
            flash(f'Contact "{contact.full_name}" added successfully!', 'success')
            return redirect(url_for('contacts_list'))
        
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating contact: {str(e)}')
            flash('An error occurred while adding the contact. Please try again.', 'error')
            return render_template('contact_form.html', contact=None, form_data=request.form)
    
    return render_template('contact_form.html', contact=None, form_data=None)

@app.route('/contacts/<int:contact_id>')
def view_contact(contact_id):
    """View contact details"""
    try:
        contact = Contact.query.get_or_404(contact_id)
        return render_template('contact_detail.html', contact=contact)
    except Exception as e:
        app.logger.error(f'Error viewing contact {contact_id}: {str(e)}')
        flash('Contact not found.', 'error')
        return redirect(url_for('contacts_list'))

@app.route('/contacts/<int:contact_id>/edit', methods=['GET', 'POST'])
def edit_contact(contact_id):
    """Edit existing contact"""
    try:
        contact = Contact.query.get_or_404(contact_id)
        
        if request.method == 'POST':
            # Validate form
            form = ContactForm(request.form)
            
            if not form.validate():
                for field, error in form.errors.items():
                    flash(f'{field.replace("_", " ").title()}: {error}', 'error')
                return render_template('contact_form.html', contact=contact, form_data=request.form)
            
            # Update contact
            cleaned_data = form.get_cleaned_data()
            for key, value in cleaned_data.items():
                setattr(contact, key, value)
            
            contact.updated_at = datetime.utcnow()
            db.session.commit()
            
            app.logger.info(f'Contact updated: {contact.full_name} (ID: {contact.id})')
            flash(f'Contact "{contact.full_name}" updated successfully!', 'success')
            return redirect(url_for('view_contact', contact_id=contact.id))
        
        return render_template('contact_form.html', contact=contact, form_data=None)
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error editing contact {contact_id}: {str(e)}')
        flash('An error occurred. Please try again.', 'error')
        return redirect(url_for('contacts_list'))

@app.route('/contacts/<int:contact_id>/delete', methods=['POST'])
def delete_contact(contact_id):
    """Delete contact"""
    try:
        contact = Contact.query.get_or_404(contact_id)
        contact_name = contact.full_name
        
        db.session.delete(contact)
        db.session.commit()
        
        app.logger.info(f'Contact deleted: {contact_name} (ID: {contact_id})')
        flash(f'Contact "{contact_name}" deleted successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting contact {contact_id}: {str(e)}')
        flash('An error occurred while deleting the contact.', 'error')
    
    return redirect(url_for('contacts_list'))

@app.route('/import-export', methods=['GET', 'POST'])
def import_export():
    """Import/Export contacts page"""
    if request.method == 'POST':
        # Handle CSV import
        if 'csv_file' not in request.files:
            flash('No file selected.', 'error')
            return redirect(url_for('import_export'))
        
        file = request.files['csv_file']
        
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(url_for('import_export'))
        
        if file and allowed_file(file.filename):
            try:
                stats = import_contacts_from_csv(file)
                
                # Display results
                flash(f'Import completed: {stats["imported"]} imported, {stats["updated"]} updated, {stats["skipped"]} skipped out of {stats["total"]} total rows.', 'success')
                
                if stats['errors']:
                    for error in stats['errors'][:5]:  # Show first 5 errors
                        flash(error, 'warning')
                    if len(stats['errors']) > 5:
                        flash(f'...and {len(stats["errors"]) - 5} more errors.', 'warning')
                
                app.logger.info(f'CSV import: {stats["imported"]} imported, {stats["updated"]} updated')
            
            except Exception as e:
                app.logger.error(f'Error importing CSV: {str(e)}')
                flash('An error occurred during import. Please check your CSV file format.', 'error')
        else:
            flash('Invalid file type. Only CSV files are allowed.', 'error')
        
        return redirect(url_for('import_export'))
    
    return render_template('import_export.html')

@app.route('/export')
def export_contacts():
    """Export all contacts to CSV"""
    try:
        contacts = Contact.query.order_by(Contact.full_name).all()
        csv_data = export_contacts_to_csv(contacts)
        
        # Create a file-like object
        output = io.BytesIO()
        output.write(csv_data.encode('utf-8'))
        output.seek(0)
        
        filename = f'contacts_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        app.logger.error(f'Error exporting contacts: {str(e)}')
        flash('An error occurred while exporting contacts.', 'error')
        return redirect(url_for('import_export'))

# Error handlers

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server error: {str(error)}')
    flash('An internal error occurred. Please try again later.', 'error')
    return render_template('index.html'), 500

# Run application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
