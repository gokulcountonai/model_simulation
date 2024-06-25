$(document).ready(function() {
    // Function to toggle blur effect on the content area
    function toggleBlur(blur) {
        $('.elements').toggleClass('blurred', blur);
    }

    // Fetch mills data on page load
    function fetchMills() {
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
                    machineMillSelect.append(`<option value="${mill.mill_id}">${mill.mill_name}</option>`);
                });
            },
            error: function(error) {
                console.error('Error fetching mill details:', error);
            }
        });
    }

    fetchMills(); // Call function to fetch mills data on page load

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
                    alert('The process is complete.');
                    window.location.href = '/'; // Redirect to home page
                } else {
                    alert(data.message); // Show error message
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $('#loader').hide(); // Hide loader
                toggleBlur(false); // Remove blur effect
                console.error('Error:', textStatus, errorThrown);
                alert('An error occurred while submitting the form.');
            }
        });
    }

    // Show modal when add button is clicked
    $('#addMillButton').click(function() {
        $('#modalContainerMill').fadeIn();
    });

    $('#addMachineButton').click(function() {
        $('#modalContainerMachine').fadeIn();
    });

    // Hide modal when clicking outside or on close button
    $(document).mouseup(function(e) {
        var modalMill = $('#modalContainerMill .modal-content');
        var modalMachine = $('#modalContainerMachine .modal-content');

        if (!modalMill.is(e.target) && modalMill.has(e.target).length === 0) {
            $('#modalContainerMill').fadeOut();
        }

        if (!modalMachine.is(e.target) && modalMachine.has(e.target).length === 0) {
            $('#modalContainerMachine').fadeOut();
        }
    });

    // Close modals when the close button is clicked
    $('.close-modal').click(function() {
        $(this).closest('.modal-container').fadeOut();
    });

    // Handle form submission
    $('#addMillForm').submit(function(e) {
        e.preventDefault();

        // Example: Get the values and do something with them
        var millName = $('#millName').val();

        // For demonstration, log the values
        console.log('Mill Name:', millName);

        // Close the modal after submission
        $('#modalContainerMill').fadeOut();
    });

    $('#addMachineForm').submit(function(e) {
        e.preventDefault();

        // Example: Get the values and do something with them
        var machineMillName = $('#machineMillName').val();
        var machineName = $('#machineName').val();

        // For demonstration, log the values
        console.log('Mill Name:', machineMillName);
        console.log('Machine Name:', machineName);

        // Close the modal after submission
        $('#modalContainerMachine').fadeOut();
    });
});

function closeModal(modalId) {
    $('#' + modalId).fadeOut();
}