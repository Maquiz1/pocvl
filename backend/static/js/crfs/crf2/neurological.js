document.addEventListener("DOMContentLoaded", function () {
    const neurologicalField = document.getElementById("id_neurological");
    const neurologicalComments = document.getElementById("neurological-comments");
    const neurologicalSignifcnt = document.getElementById("neurological-signifcnt");

    function toggleneurologicalFields() {
        if (neurologicalField.value === "2") {
            neurologicalComments.style.display = "table-cell";
            neurologicalSignifcnt.style.display = "table-cell";
        } else {
            neurologicalComments.style.display = "none";
            neurologicalSignifcnt.style.display = "none";
        }
    }

    // Run on load
    toggleneurologicalFields();

    // Run on change
    neurologicalField.addEventListener("change", toggleneurologicalFields);
});
