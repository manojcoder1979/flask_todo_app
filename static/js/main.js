document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle functionality
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const toggleBtn = document.getElementById('toggleSidebar');

    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('expanded');
        
        // Store sidebar state in localStorage
        const isCollapsed = sidebar.classList.contains('collapsed');
        localStorage.setItem('sidebarCollapsed', isCollapsed);
    });

    // Restore sidebar state on page load
    const isCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (isCollapsed) {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
    }

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredInputs = form.querySelectorAll('input[required]');
            let isValid = true;

            requiredInputs.forEach(input => {``
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });

    // Delete confirmation
    const deleteBtns = document.querySelectorAll('.delete-btn');
    deleteBtns.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Are you sure want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // Number input validation
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            if (this.value < 0) {
                this.value = 0;
            }
        });
    });

    // Highlight newly added or edited rows
    const highlightRow = (rowId) => {
        const row = document.getElementById(rowId);
        if (row) {
            row.classList.add('row-highlight');
            // Remove class after animation completes
            setTimeout(() => {
                row.classList.remove('row-highlight');
            }, 3000);
        }
    };

    // Get URL parameters to check for newly added/edited items
    const urlParams = new URLSearchParams(window.location.search);
    const newItemId = urlParams.get('highlight');
    if (newItemId) {
        highlightRow(`row-${newItemId}`);
    }

    // Add scroll shadows to table
    const tableWrapper = document.querySelector('.table-wrapper');
    if (tableWrapper) {
        const handleScroll = () => {
            const maxScroll = tableWrapper.scrollWidth - tableWrapper.clientWidth;
            tableWrapper.classList.toggle('shadow-left', tableWrapper.scrollLeft > 0);
            tableWrapper.classList.toggle('shadow-right', tableWrapper.scrollLeft < maxScroll);
        };

        tableWrapper.addEventListener('scroll', handleScroll);
        // Initial check
        handleScroll();
    }
});
