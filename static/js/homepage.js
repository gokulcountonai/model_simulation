$(document).ready(function() {
    // Function to toggle blur class
    function toggleBlur(blur) {
        $('.elements').toggleClass('blurred', blur);
    }

    // Function to fetch mill names and populate dropdowns
    function fetchMillNames() {
        $.ajax({
            url: '/mills',
            method: 'GET',
            success: function(data) {
                const millSelect = $('#mill');
                const machineMillSelect = $('#machineMillName');
                millSelect.html('<option value="" disabled selected>Select mill</option>');
                machineMillSelect.html('<option value="" disabled selected>Select mill</option>');

                data.forEach(function(mill) {
                    millSelect.append(`<option value="${mill.mill_id}">${mill.mill_name}</option>`);
                    machineMillSelect.append(`<option value="${mill.mill_name}">${mill.mill_name}</option>`);
                });
            },
            error: function(error) {
                console.error('Error fetching mill details:', error);
            }
        });
    }

    // Initial fetch of mill names
    fetchMillNames();

    // Handler for change in mill dropdown
    $('#mill').change(function() {
        const selectedMillId = $(this).val();
        $.ajax({
            url: `/machines_by_mill/${selectedMillId}`,
            method: 'GET',
            success: function(data) {
                const machineSelect = $('#machine');
                machineSelect.html('<option value="" disabled selected>Select machine</option>');

                data.forEach(function(machineName) {
                    machineSelect.append(`<option value="${machineName}">${machineName}</option>`);
                });
            },
            error: function(error) {
                console.error('Error fetching machines for selected mill:', error);
            }
        });
    });

    // Submit event handler for stimulation form
    $('#stimulationForm').submit(function(event) {
        event.preventDefault();
        var score = $('#score').val();
        var fps = $('#fps').val();

        if (!(score >= 0 && score <= 1)) {
            alert('Score must be between 0 and 1.');
            return;
        }

        if (!(fps >= 10 && fps <= 40)) {
            alert('FPS must be between 10 and 40.');
            return;
        }

        submitForm();
    });

    // Function to submit form data
    function submitForm() {
        $('#loader').show();
        toggleBlur(true);
    
        var formData = new FormData($('#stimulationForm')[0]);
    
        $.ajax({
            url: '/submit-form',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(data) {
                $('#loader').hide(); // Hide loader
                toggleBlur(false); // Remove blur effect
                if (data.status === 'success') {
                    alert('The process is complete.');
                    if (data.report === 'yes') {
                        window.location.href = '/';
                    } else {
                        window.location.href = '/';
                    }
                } else {
                    alert(data.message); // Show error message
                }
            },
            error: function(error) {
                $('#loader').hide(); // Hide loader on error
                toggleBlur(false); // Remove blur effect on error
                console.error('Error submitting form:', error);
                alert('An error occurred while submitting the form. Please try again.');
            }
        });
    }

    // Show modal for adding mill
    $('#addMillButton').click(function() {
        $('#modalContainerMill').show();
    });

    // Show modal for adding machine
    $('#addMachineButton').click(function() {
        $('#modalContainerMachine').show();
    });

    // Close modals when clicking the close button (x)
    $('.close').click(function() {
        $(this).closest('.modal-container').hide();
    });

    // Close modals when clicking outside the modal content
    $(window).click(function(event) {
        if ($(event.target).hasClass('modal-container')) {
            $(event.target).hide();
        }
    });

    // Submit event handler for adding mill form
    $('#addMillForm').submit(function(e) {
        e.preventDefault();
        var millName = $('#millName').val();
        $.ajax({
            url: '/add-mill',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ name: millName }),
            success: function(response) {
                $('#modalContainerMill').hide();
                location.reload();
            },
            error: function(error) {
                console.error('Error adding mill:', error);
                alert('An error occurred while adding the mill. Please try again.');
            }
        });
    });

    // Submit event handler for adding machine form
    $('#addMachineForm').submit(function(e) {
        e.preventDefault();
        var machineMillName = $('#machineMillName').val();
        var machineName = $('#machineName').val();
        $.ajax({
            url: '/add-machine',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ mill_name: machineMillName, machine_name: machineName }),
            success: function(response) {
                $('#modalContainerMachine').hide();
                location.reload();
            },
            error: function(error) {
                console.error('Error adding machine:', error);
                alert('An error occurred while adding the machine. Please try again.');
            }
        });
    });
});
