// Delete confirmation modal
function confirmDelete(contactId, contactName) {
    const modal = document.getElementById('deleteModal');
    const form = document.getElementById('deleteForm');
    const nameElement = document.getElementById('contactName');
    
    // Set contact name in modal
    nameElement.textContent = contactName;
    
    // Set form action to delete URL
    form.action = `/contacts/${contactId}/delete`;
    
    // Show modal
    modal.classList.add('active');
}

function closeDeleteModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('active');
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('deleteModal');
    if (event.target === modal) {
        closeDeleteModal();
    }
}

// File input name display
function updateFileName(input) {
    const fileNameSpan = document.getElementById('fileName');
    if (input.files.length > 0) {
        fileNameSpan.textContent = input.files[0].name;
    } else {
        fileNameSpan.textContent = 'No file chosen';
    }
}

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

// Form validation enhancement
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('.contact-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const phoneInput = form.querySelector('#phone_number');
            const phone = phoneInput.value.trim();
            
            // Basic phone validation
            if (phone.length < 10) {
                e.preventDefault();
                alert('Phone number must be at least 10 digits long.');
                phoneInput.focus();
                return false;
            }
        });
    });
});
