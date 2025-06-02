function openAddModal() {
    const modal = document.getElementById('supplierModal');
    const form = document.getElementById('supplierForm');
    const title = document.getElementById('modalTitle');
    
    title.textContent = 'Add Supplier';
    form.reset();
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('supplierModal');
    modal.style.display = 'none';
}

function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    fetch('/suppliers', {
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

function editSupplier(id) {
    fetch(`/suppliers/${id}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('supplierModal');
            const form = document.getElementById('supplierForm');
            const title = document.getElementById('modalTitle');
            
            title.textContent = 'Edit Supplier';
            
            // Populate form fields
            Object.keys(data).forEach(key => {
                const input = form.elements[key];
                if (input) input.value = data[key];
            });
            
            modal.style.display = 'block';
        });
}

function deleteSupplier(id) {
    if (confirm('Are you sure you want to delete this supplier?')) {
        fetch(`/suppliers/${id}`, {
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
    const modal = document.getElementById('supplierModal');
    if (event.target === modal) {
        closeModal();
    }
}