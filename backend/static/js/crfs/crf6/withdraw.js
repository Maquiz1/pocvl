document.addEventListener("DOMContentLoaded", function () {

    const withdrewField = document.getElementById("id_withdrew_reason");
    const withdrewOtherDiv = document.getElementById("div_withdrew_other");

    function toggleWithdrewOther() {

        if (!withdrewField) return;

        const value = withdrewField.value;

        // RESET
        if (withdrewOtherDiv) withdrewOtherDiv.style.display = "none";

        // SHOW ONLY IF = 5
        if (value === "5") {
            if (withdrewOtherDiv) withdrewOtherDiv.style.display = "block";
        }

        // 🔥 OPTIONAL: CLEAR WHEN HIDDEN
        if (withdrewOtherDiv && withdrewOtherDiv.style.display === "none") {
            const field = document.getElementById("id_withdrew_other");
            if (field) field.value = "";
        }
    }

    // INITIAL
    toggleWithdrewOther();

    // EVENT
    if (withdrewField) {
        withdrewField.addEventListener("change", toggleWithdrewOther);
    }

});