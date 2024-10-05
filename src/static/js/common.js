$(document).ready(function () {
    // Handle the modal form submission for add or edit
    $(document).on('submit', '.modal-form', function(e) {
        e.preventDefault();  // Prevent the default form submission

        var form = $(this);
        var url = form.attr('action');  // Get the URL from the form's action attribute

        $.ajax({
            type: form.attr('method'),  // Use the method specified in the form (GET or POST)
            url: url,
            data: form.serialize(),  // Serialize form data for AJAX submission
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    $('.modal').modal('hide');  // Hide the modal after successful submission
                    $('.modal-backdrop').remove();  // Remove the backdrop to prevent overlaps
                    loadContent(form.data('entity'));  // Reload the table content (custom function)
                } else {
                    alert('Error: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                alert('Failed to submit form. Error: ' + error);
            }
        });
    });

    // Handle the search form submission using AJAX
    $(document).on('submit', '#searchForm', function(e) {
        e.preventDefault();  // Prevent the default form submission

        var form = $(this);
        $.ajax({
            type: 'GET',
            url: form.attr('action'),  // Use the form's action attribute (URL for searching)
            data: form.serialize(),  // Serialize form data for AJAX submission
            success: function(response) {
                var contentId = form.data('entity') + '-content';
                $('#' + contentId).html(response);  // Replace content with the updated search results
            },
            error: function(xhr, status, error) {
                console.error("Error during search submission:", error);
                alert("Failed to search. Error: " + error);
            }
        });
    });

    // Handle the delete button click event
    $(document).on('submit', '.delete-form', function(e) {
        e.preventDefault();  // Prevent the default form submission

        var form = $(this);
        $.ajax({
            type: 'POST',
            url: form.attr('action'),  // Get the URL from the form's action attribute
            data: form.serialize(),  // Serialize form data for AJAX submission
            success: function(response) {
                if (response.success) {
                    alert(response.message);
                    loadContent(form.data('entity'));  // Refresh the corresponding content (students, colleges, etc.)
                } else {
                    alert('Error: ' + response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error("Error during delete submission:", error);
                alert("Failed to delete. Error: " + error);
            }
        });
    });

    // Reset form and remove readonly on code fields when the modal is hidden
    $('.modal').on('hidden.bs.modal', function () {
        $(this).find('form')[0].reset();  // Reset form fields
        const codeField = $(this).find('form input[name="code"]')[0];
        if (codeField) {
            codeField.readOnly = false;  // Ensure code field is editable when the modal is closed
        }
    });
});

// Function to dynamically load content for a specific entity
function loadContent(entity) {
    console.log("Loading " + entity + " table...");
    var url = '/' + entity;

    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            $('#' + entity + '-content').html(response);
        },
        error: function (xhr, status, error) {
            console.error("Error loading content for " + entity + ": " + error);
        }
    });
}
