$(document).ready(function () {
    // Automatically load the students content on page load
    loadTabContent('students', '/students');

    // Event listener for tab clicks
    $('#entityTabs a').on('click', function (event) {
        event.preventDefault();
        let targetTab = $(this).attr('href').substring(1); // Get the ID of the tab without #
        let url = '';

        if (targetTab === 'students') {
            url = '/students';
        } else if (targetTab === 'programs') {
            url = '/programs';
        } else if (targetTab === 'colleges') {
            url = '/colleges';
        }

        if (url) {
            loadTabContent(targetTab, url);
        }
    });
});

// Load content for a specific tab via AJAX
function loadTabContent(targetTab, url) {
    $.ajax({
        url: url,
        type: 'GET',
        success: function (response) {
            $('#' + targetTab + '-content').html(response);
        },
        error: function (xhr, status, error) {
            console.error("Error loading content for " + targetTab + ": " + error);
        }
    });
}