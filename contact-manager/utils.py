import csv
import io
import logging
from datetime import datetime
from models import Contact, db

logger = logging.getLogger(__name__)

def export_contacts_to_csv(contacts):
    """Export contacts to CSV format"""
    try:
        output = io.StringIO()
        fieldnames = ['full_name', 'phone_number', 'email', 'address', 'company', 'notes']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        for contact in contacts:
            writer.writerow({
                'full_name': contact.full_name,
                'phone_number': contact.phone_number,
                'email': contact.email,
                'address': contact.address or '',
                'company': contact.company or '',
                'notes': contact.notes or ''
            })
        
        logger.info(f'Exported {len(contacts)} contacts to CSV')
        return output.getvalue()
    except Exception as e:
        logger.error(f'Error exporting contacts to CSV: {str(e)}')
        raise

def import_contacts_from_csv(file_stream):
    """Import contacts from CSV file"""
    stats = {
        'total': 0,
        'imported': 0,
        'updated': 0,
        'skipped': 0,
        'errors': []
    }
    
    try:
        # Read CSV file
        stream = io.StringIO(file_stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)
        
        for row_num, row in enumerate(reader, start=2):
            stats['total'] += 1
            
            try:
                # Validate required fields
                if not row.get('full_name') or not row.get('phone_number') or not row.get('email'):
                    stats['skipped'] += 1
                    stats['errors'].append(f"Row {row_num}: Missing required fields")
                    continue
                
                # Check for duplicate by email
                existing = Contact.query.filter_by(email=row['email'].strip().lower()).first()
                
                if existing:
                    # Update existing contact
                    existing.full_name = row['full_name'].strip()
                    existing.phone_number = row['phone_number'].strip()
                    existing.address = row.get('address', '').strip() or None
                    existing.company = row.get('company', '').strip() or None
                    existing.notes = row.get('notes', '').strip() or None
                    existing.updated_at = datetime.utcnow()
                    stats['updated'] += 1
                else:
                    # Create new contact
                    contact = Contact(
                        full_name=row['full_name'].strip(),
                        phone_number=row['phone_number'].strip(),
                        email=row['email'].strip().lower(),
                        address=row.get('address', '').strip() or None,
                        company=row.get('company', '').strip() or None,
                        notes=row.get('notes', '').strip() or None
                    )
                    db.session.add(contact)
                    stats['imported'] += 1
            
            except Exception as e:
                stats['skipped'] += 1
                stats['errors'].append(f"Row {row_num}: {str(e)}")
                logger.error(f"Error importing row {row_num}: {str(e)}")
        
        # Commit all changes
        db.session.commit()
        logger.info(f"CSV import completed: {stats['imported']} imported, {stats['updated']} updated, {stats['skipped']} skipped")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f'Error importing CSV: {str(e)}')
        stats['errors'].append(f"File error: {str(e)}")
    
    return stats

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}
