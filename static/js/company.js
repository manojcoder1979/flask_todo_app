function handleSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData);
    
    fetch('/company', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Company information saved successfully');
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving');
    });
}

// Form validation
document.getElementById('companyForm').addEventListener('submit', function(e) {
    const pincode = document.getElementById('pincode').value;
    if (!/^\d{6}$/.test(pincode)) {
        alert('Please enter a valid 6-digit PIN code');
        e.preventDefault();
    }
});