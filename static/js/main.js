// Main JavaScript file for Resume Reviewer AI

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // File upload validation
    const fileUpload = document.querySelector('.drop-zone__input');
    if (fileUpload) {
        fileUpload.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Check file type
                const fileType = file.type;
                if (fileType !== 'application/pdf') {
                    alert('Only PDF files are allowed.');
                    e.target.value = '';
                    return;
                }

                // Check file size (max 16MB)
                const fileSize = file.size / 1024 / 1024; // Convert to MB
                if (fileSize > 16) {
                    alert('File size exceeds 16MB. Please upload a smaller file.');
                    e.target.value = '';
                    return;
                }
            }
        });
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Progress bar animation
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(progressBar => {
        const value = progressBar.getAttribute('aria-valuenow');
        progressBar.style.width = '0%';
        setTimeout(() => {
            progressBar.style.width = value + '%';
        }, 200);
    });

    // Keyword table search/filter
    const keywordFilter = document.getElementById('keywordFilter');
    if (keywordFilter) {
        keywordFilter.addEventListener('input', function() {
            const filterValue = this.value.toLowerCase();
            const keywordRows = document.querySelectorAll('.keyword-table tbody tr');
            
            keywordRows.forEach(row => {
                const keyword = row.querySelector('td:first-child').textContent.toLowerCase();
                if (keyword.includes(filterValue)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Print functionality for resume results
    const printButton = document.getElementById('printResults');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
}); 