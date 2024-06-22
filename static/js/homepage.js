$(document).ready(function() {
    // Fetch machines and mills data on page load
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

    // Event listener for mill selection change
    $('#mill').change(function() {
        const selectedMillId = $(this).val(); // Get selected mill ID
        $.ajax({
            url: `/machines_by_mill/${selectedMillId}`, // Assuming this endpoint exists
            method: 'GET',
            success: function(data) {
                const machineSelect = $('#machine');
                machineSelect.html('<option value="" disabled selected>Select machine</option>'); // Clear and add placeholder
                data.forEach(function(machineName) {
                    // Assuming machineName is a string like 'hisar 1', 'hisar 2'
                    machineSelect.append(`<option value="${machineName}">${machineName}</option>`);
                });
            },
            error: function(error) {
                console.error('Error fetching machines for selected mill:', error);
            }
        });
    });

    // Form submission handling
    $('#stimulationForm').submit(function(event) {
        var score = $('#score').val();
        var fps = $('#fps').val();

        // Validate score
        if (!(score >= 0 && score <= 10)) {
            alert('Score must be between 0 and 10.');
            event.preventDefault(); // Prevent form submission
            return;
        }

        // Validate fps
        if (!(fps >= 10 && fps <= 40)) {
            alert('FPS must be between 10 and 40.');
            event.preventDefault(); // Prevent form submission
            return;
        }

        // If validation passes, form will submit normally
    });
});
