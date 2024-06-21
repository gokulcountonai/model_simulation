// Event listener for form submission
document.getElementById('stimulationForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    // Convert form data to dictionary format
    const formData = {};
    const inputs = this.querySelectorAll('input, select');
    inputs.forEach(input => {
        formData[input.name] = input.value;
    });

    // Output the dictionary (for demonstration purposes)
    console.log(formData);

    // Send formData to Flask backend using AJAX
    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert(JSON.stringify(data, null, 2));
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Error occurred. Please try again.');
    });
});
