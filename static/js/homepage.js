$(document).ready(function() {
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

    $('#stimulationForm').on('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(this);

        $.ajax({
            url: '/submit',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                console.log('Success:', data);
                alert(JSON.stringify(data, null, 2)); // Display response data in an alert
            },
            error: function(error) {
                console.error('Error:', error);
                alert('Error occurred. Please try again.');
            }
        });
    });
});
