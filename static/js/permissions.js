function openAddModal() {
    const modal = document.getElementById('permissionModal');
    const form = document.getElementById('permissionForm');
    const title = document.getElementById('modalTitle');
    
    title.textContent = 'Add Permission';
    form.reset();
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('permissionModal');
    modal.style.display = 'none';
}

function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    fetch('/permissions', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.message);
        }
    });
}

function editPermission(id) {
    fetch(`/permissions/${id}`)
        .then(response => response.json())
        .then(data => {
            const modal = document.getElementById('permissionModal');
            const form = document.getElementById('permissionForm');
            const title = document.getElementById('modalTitle');
            
            title.textContent = 'Edit Permission';
            document.getElementById('name').value = data.name;
            document.getElementById('description').value = data.description;
            document.getElementById('module').value = data.module;
            
            modal.style.display = 'block';
        });
}

function deletePermission(id) {
    if (confirm('Are you sure you want to delete this permission?')) {
        fetch(`/permissions/${id}`, {
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
    const modal = document.getElementById('permissionModal');
    if (event.target === modal) {
        closeModal();
    }
}