$(document).ready(function() {
    // Fetch machine details and populate the select element
    $.ajax({
        url: '/machines',
        method: 'GET',
        success: function(data) {
            const machineSelect = $('#machine');
            machineSelect.html('<option value="" disabled selected>Select machine</option>');
            data.forEach(function(machine) {
                machineSelect.append(`<option value="${machine.machine_id}">${machine.machine_name}</option>`);
            });
        },
        error: function(error) {
            console.error('Error fetching machine details:', error);
        }
    });

    // Fetch mill details and populate the select element
    $.ajax({
        url: '/mills',
        method: 'GET',
        success: function(data) {
            const millSelect = $('#mill');
            millSelect.html('<option value="" disabled selected>Select mill</option>');
            data.forEach(function(mill) {
                millSelect.append(`<option value="${mill.mill_id}">${mill.mill_name}</option>`);
            });
        },
        error: function(error) {
            console.error('Error fetching mill details:', error);
        }
    });

    // Event listener for form submission
    $('#stimulationForm').on('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        const formData = {};
        $(this).find('input, select').each(function() {
            formData[this.name] = $(this).val();
        });

        // Send formData to Flask backend using AJAX
        $.ajax({
            url: '/submit',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(data) {
                console.log('Success:', data);
                alert(JSON.stringify(data, null, 2)); // Display response data in an alert
                
                // Now insert the processed data into the database
                $.ajax({
                    url: '/insert_validation_log',
                    method: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify(data.data), // Sending the processed data
                    success: function(insertData) {
                        console.log('Insertion Success:', insertData);
                        alert('Data inserted successfully');
                    },
                    error: function(error) {
                        console.error('Insertion Error:', error);
                        alert('Error occurred during insertion. Please try again.');
                    }
                });
            },
            error: function(error) {
                console.error('Error:', error);
                alert('Error occurred. Please try again.');
            }
        });
    });
});

