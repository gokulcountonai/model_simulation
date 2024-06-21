document.addEventListener('DOMContentLoaded', (event) => {
    const typeValSelect = document.getElementById('typeval');
    const selectedOptionsDiv = document.getElementById('selectedOptions');

    // Function to update the displayed selected options
    function updateSelectedOptions() {
        selectedOptionsDiv.innerHTML = ''; // Clear previous selections
        Array.from(typeValSelect.selectedOptions).forEach(option => {
            const div = document.createElement('div');
            div.className = 'selected-option';
            div.textContent = option.text;

            // Create the remove button
            const removeBtn = document.createElement('button');
            removeBtn.textContent = 'x';
            removeBtn.className = 'remove-btn';
            removeBtn.onclick = () => removeOption(option.value);

            // Append the remove button to the div
            div.appendChild(removeBtn);

            // Append the div to the selectedOptionsDiv
            selectedOptionsDiv.appendChild(div);
        });
    }

    // Function to remove an option from the selection
    function removeOption(value) {
        const options = typeValSelect.options;
        for (let i = 0; i < options.length; i++) {
            if (options[i].value === value) {
                options[i].selected = false;
                break;
            }
        }
        updateSelectedOptions();
    }

    // Event listener for the select element
    typeValSelect.addEventListener('change', function() {
        updateSelectedOptions();
    });

    // Initial update of the selected options display
    updateSelectedOptions();
});
