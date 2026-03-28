document.addEventListener("DOMContentLoaded", function () {
    const abdominalField = document.getElementById("id_abdominal");
    const abdominalComments = document.getElementById("abdominal-comments");
    const abdominalSignifcnt = document.getElementById("abdominal-signifcnt");

    function toggleabdominalFields() {
        if (abdominalField.value === "2") {
            abdominalComments.style.display = "table-cell";
            abdominalSignifcnt.style.display = "table-cell";
        } else {
            abdominalComments.style.display = "none";
            abdominalSignifcnt.style.display = "none";
        }
    }

    // Run on load
    toggleabdominalFields();

    // Run on change
    abdominalField.addEventListener("change", toggleabdominalFields);
});
