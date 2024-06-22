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
});


