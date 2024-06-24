$(document).ready(function() {
    // Function to toggle blur effect on the content area
    function toggleBlur(blur) {
        $('.elements').toggleClass('blurred', blur);
    }

    // Fetch mills data on page load
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

    // Form submission handling
    $('#stimulationForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        var score = $('#score').val();
        var fps = $('#fps').val();

        // Validate score
        if (!(score >= 0 && score <= 1)) {
            alert('Score must be between 0 and 1.');
            return;
        }

        // Validate fps
        if (!(fps >= 10 && fps <= 40)) {
            alert('FPS must be between 10 and 40.');
            return;
        }

        // If validation passes, continue with form submission
        submitForm();
    });

    // Function to handle form submission via AJAX
    function submitForm() {
        // Show loader and blur background
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
                    // Show a completion message with an alert
                    alert('The process is complete.');
                    // After clicking "OK", check the report value for redirection
                    if (data.report === 'yes') {
                        window.location.href = '/';
                    } else {
                        window.location.href = '/';
                    }
                } else {
                    // If not successful, show the error message from the response
                    alert(data.message); // Show error message
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $('#loader').hide(); // Hide loader
                toggleBlur(false); // Remove blur effect
                console.error('Error:', textStatus, errorThrown);
                // Show a generic error message
                alert('An error occurred while submitting the form.');
            }
        });
    }
});
