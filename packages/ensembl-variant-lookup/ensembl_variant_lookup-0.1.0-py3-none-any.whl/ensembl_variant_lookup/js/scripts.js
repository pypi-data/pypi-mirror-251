// scripts.js

$(document).ready(function() {
    // Activate DataTable on the table with Buttons extension
    $('#variantTable').DataTable({
        dom: 'Bfrtip',
        buttons: [
            'copy', 'csv', 'excel', 'pdf', 'print'
        ]
    });

    // Get the id parameter from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get('id');

    // If id is available, set it as the value of the rsid input field
    if (id) {
        document.getElementById('rsid').value = id;
    }
});
