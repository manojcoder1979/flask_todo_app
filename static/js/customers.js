function openAddModal() {
    const modal = document.getElementById('customerModal');
    const form = document.getElementById('customerForm');
    const title = document.getElementById('modalTitle');
    
    title.textContent = 'Add Customer';
    form.reset();
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('customerModal');
    modal.style.display = 'none';
}

function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    fetch('/customers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.message);
        }
    });
}

function editCustomer(id) {
    fetch(`/customers/${id}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('customerModal');
            const form = document.getElementById('customerForm');
            const title = document.getElementById('modalTitle');
            
            title.textContent = 'Edit Customer';
            
            // Populate form fields
            Object.keys(data).forEach(key => {
                const input = form.elements[key];
                if (input) input.value = data[key];
            });
            
            modal.style.display = 'block';
        });
}

function deleteCustomer(id) {
    if (confirm('Are you sure you want to delete this customer?')) {
        fetch(`/customers/${id}`, {
            method: 'DELETE'
        }).then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    }
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('customerModal');
    if (event.target === modal) {
        closeModal();
    }
}