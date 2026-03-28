document.addEventListener("DOMContentLoaded", function () {
    const cardiovascularField = document.getElementById("id_cardiovascular");
    const cardiovascularComments = document.getElementById("cardiovascular-comments");
    const cardiovascularSignifcnt = document.getElementById("cardiovascular-signifcnt");

    function togglecardiovascularFields() {
        if (cardiovascularField.value === "2") {
            cardiovascularComments.style.display = "table-cell";
            cardiovascularSignifcnt.style.display = "table-cell";
        } else {
            cardiovascularComments.style.display = "none";
            cardiovascularSignifcnt.style.display = "none";
        }
    }

    // Run on load
    togglecardiovascularFields();

    // Run on change
    cardiovascularField.addEventListener("change", togglecardiovascularFields);
});
