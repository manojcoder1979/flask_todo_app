function openAddModal() {
    const modal = document.getElementById('roleModal');
    const form = document.getElementById('roleForm');
    const title = document.getElementById('modalTitle');
    
    title.textContent = 'Add Role';
    form.reset();
    modal.style.display = 'block';
}

function closeModal() {
    const modal = document.getElementById('roleModal');
    modal.style.display = 'none';
}

function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    fetch('/roles', {
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

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('roleModal');
    if (event.target === modal) {
        closeModal();
    }
}