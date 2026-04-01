// Admin Panel JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Confirm dialog for destructive actions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const deleteBtn = this.querySelector('button[name="action"][value="delete"]');
            if (e.submitter === deleteBtn) {
                const username = this.parentElement.textContent.trim().split('\n')[0];
                if (!confirm(`Are you sure you want to delete this user? This action cannot be undone.`)) {
                    e.preventDefault();
                }
            }
        });
    });

    // Table row hover effects
    const rows = document.querySelectorAll('table tbody tr');
    rows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.boxShadow = 'inset 0 0 10px rgba(0, 0, 0, 0.05)';
        });
        row.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'none';
        });
    });
});

// Function to format large numbers
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num;
}

// Function to update stats dynamically (for future use)
function updateStats(endpoint) {
    fetch(endpoint)
        .then(response => response.json())
        .then(data => {
            // Update stat cards
            Object.keys(data).forEach(key => {
                const element = document.querySelector(`[data-stat="${key}"]`);
                if (element) {
                    element.textContent = formatNumber(data[key]);
                    element.classList.add('updated');
                }
            });
        })
        .catch(error => console.error('Error:', error));
}
