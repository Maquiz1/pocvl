document.addEventListener("DOMContentLoaded", function () {
    const AppearanceField = document.getElementById("id_appearance");
    const appearanceComments = document.getElementById("appearance-comments");
    const appearanceSignifcnt = document.getElementById("appearance-signifcnt");

    function toggleAppearanceFields() {
        if (AppearanceField.value === "2") {
            appearanceComments.style.display = "table-cell";
            appearanceSignifcnt.style.display = "table-cell";
        } else {
            appearanceComments.style.display = "none";
            appearanceSignifcnt.style.display = "none";
        }
    }

    // Run on load
    toggleAppearanceFields();

    // Run on change
    AppearanceField.addEventListener("change", toggleAppearanceFields);
});
