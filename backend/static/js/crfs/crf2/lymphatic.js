document.addEventListener("DOMContentLoaded", function () {
    const lymphaticField = document.getElementById("id_lymphatic");
    const lymphaticComments = document.getElementById("lymphatic-comments");
    const lymphaticSignifcnt = document.getElementById("lymphatic-signifcnt");

    function togglelymphaticFields() {
        if (lymphaticField.value === "2") {
            lymphaticComments.style.display = "table-cell";
            lymphaticSignifcnt.style.display = "table-cell";
        } else {
            lymphaticComments.style.display = "none";
            lymphaticSignifcnt.style.display = "none";
        }
    }

    // Run on load
    togglelymphaticFields();

    // Run on change
    lymphaticField.addEventListener("change", togglelymphaticFields);
});
