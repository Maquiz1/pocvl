document.addEventListener("DOMContentLoaded", function () {
    const respiratoryField = document.getElementById("id_respiratory");
    const respiratoryComments = document.getElementById("respiratory-comments");
    const respiratorySignifcnt = document.getElementById("respiratory-signifcnt");

    function togglerespiratoryFields() {
        if (respiratoryField.value === "2") {
            respiratoryComments.style.display = "table-cell";
            respiratorySignifcnt.style.display = "table-cell";
        } else {
            respiratoryComments.style.display = "none";
            respiratorySignifcnt.style.display = "none";
        }
    }

    // Run on load
    togglerespiratoryFields();

    // Run on change
    respiratoryField.addEventListener("change", togglerespiratoryFields);
});
