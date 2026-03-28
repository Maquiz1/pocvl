document.addEventListener("DOMContentLoaded", function () {
    const urogenitalField = document.getElementById("id_urogenital");
    const urogenitalComments = document.getElementById("urogenital-comments");
    const urogenitalSignifcnt = document.getElementById("urogenital-signifcnt");

    function toggleurogenitalFields() {
        if (urogenitalField.value === "2") {
            urogenitalComments.style.display = "table-cell";
            urogenitalSignifcnt.style.display = "table-cell";
        } else {
            urogenitalComments.style.display = "none";
            urogenitalSignifcnt.style.display = "none";
        }
    }

    // Run on load
    toggleurogenitalFields();

    // Run on change
    urogenitalField.addEventListener("change", toggleurogenitalFields);
});
