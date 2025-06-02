function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    fetch('/add-item', {
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

function editItem(id) {
    fetch(`/add-item/${id}`)
        .then(response => response.json())
        .then(data => {
            const form = document.getElementById('itemForm');
            Object.keys(data).forEach(key => {
                const input = form.elements[key];
                if (input) input.value = data[key];
            });
            form.querySelector('button[type="submit"]').textContent = 'Update Item';
            form.onsubmit = (e) => handleUpdate(e, id);
        });
}

function handleUpdate(event, id) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    fetch(`/add-item/${id}`, {
        method: 'PUT',
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

function deleteItem(id) {
    if (confirm('Are you sure you want to delete this item?')) {
        fetch(`/add-item/${id}`, {
            method: 'DELETE'
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
}