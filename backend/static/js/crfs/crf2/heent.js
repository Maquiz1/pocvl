document.addEventListener("DOMContentLoaded", function () {
    const heentField = document.getElementById("id_heent");
    const heentComments = document.getElementById("heent-comments");
    const heentSignifcnt = document.getElementById("heent-signifcnt");

    function toggleheentFields() {
        if (heentField.value === "2") {
            heentComments.style.display = "table-cell";
            heentSignifcnt.style.display = "table-cell";
        } else {
            heentComments.style.display = "none";
            heentSignifcnt.style.display = "none";
        }
    }

    // Run on load
    toggleheentFields();

    // Run on change
    heentField.addEventListener("change", toggleheentFields);
});
