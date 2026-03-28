document.addEventListener("DOMContentLoaded", function () {
    const skinField = document.getElementById("id_skin");
    const skinComments = document.getElementById("skin-comments");
    const skinSignifcnt = document.getElementById("skin-signifcnt");

    function toggleskinFields() {
        if (skinField.value === "2") {
            skinComments.style.display = "table-cell";
            skinSignifcnt.style.display = "table-cell";
        } else {
            skinComments.style.display = "none";
            skinSignifcnt.style.display = "none";
        }
    }

    // Run on load
    toggleskinFields();

    // Run on change
    skinField.addEventListener("change", toggleskinFields);
});
