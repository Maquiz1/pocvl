document.addEventListener("DOMContentLoaded", function () {
    const psychologicalField = document.getElementById("id_psychological");
    const psychologicalComments = document.getElementById("psychological-comments");
    const psychologicalSignifcnt = document.getElementById("psychological-signifcnt");

    function togglepsychologicalFields() {
        if (psychologicalField.value === "2") {
            psychologicalComments.style.display = "table-cell";
            psychologicalSignifcnt.style.display = "table-cell";
        } else {
            psychologicalComments.style.display = "none";
            psychologicalSignifcnt.style.display = "none";
        }
    }

    // Run on load
    togglepsychologicalFields();

    // Run on change
    psychologicalField.addEventListener("change", togglepsychologicalFields);
});
