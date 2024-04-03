function cancelForm() {
    var landingPageUrl = document.getElementById('bursaryForm').getAttribute('data-landing-page-url');
    if (confirm("Are you sure you want to cancel? Any unsaved data will be lost.")) {
        window.location.href = landingPageUrl;
    }
}

function clearForm() {
    if (confirm("Are you sure you want to clear the form? Any unsaved data will be lost.")) {
        document.getElementById('bursaryForm').reset();
    }
}
