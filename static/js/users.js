function openAddModal() {
    const modal = document.getElementById('userModal');
    const form = document.getElementById('userForm');
    const title = document.getElementById('modalTitle');
    
    title.textContent = 'Add User';
    form.reset();
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('userModal');
    modal.style.display = 'none';
}

function editUser(userId) {
    const modal = document.getElementById('userModal');
    const title = document.getElementById('modalTitle');
    
    title.textContent = 'Edit User';
    
    // Fetch user data and populate form
    fetch(`/users/${userId}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('username').value = data.username;
            document.getElementById('email').value = data.email;
            document.getElementById('role').value = data.role;
        });
    
    modal.style.display = 'block';
}

function deleteUser(userId) {
    if (confirm('Are you sure you want to delete this user?')) {
        fetch(`/users/${userId}`, {
            method: 'DELETE',
        }).then(response => {
            if (response.ok) {
                location.reload();
            }
        });
    }
}

function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    fetch('/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(response => {
        if (response.ok) {
            closeModal();
            location.reload();
        }
    });
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('userModal');
    if (event.target === modal) {
        closeModal();
    }
}