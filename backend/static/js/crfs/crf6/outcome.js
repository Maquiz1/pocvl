document.addEventListener("DOMContentLoaded", function () {

    const outcomeField = document.getElementById("id_outcome");

    const outcomeDateDiv = document.getElementById("div_outcome_date");
    const outcomeOtherDiv = document.getElementById("div_outcome_other");

    function toggleOutcomeFields() {

        if (!outcomeField) return;

        const value = outcomeField.value;

        // RESET
        if (outcomeDateDiv) outcomeDateDiv.style.display = "none";
        if (outcomeOtherDiv) outcomeOtherDiv.style.display = "none";

        // =========================
        // 1,2,3,4,6 → SHOW DATE
        // =========================
        if (["1", "2", "3", "4", "6"].includes(value)) {
            if (outcomeDateDiv) outcomeDateDiv.style.display = "block";
        }

        // =========================
        // 7 → SHOW OTHER
        // =========================
        if (value === "7") {
            if (outcomeOtherDiv) outcomeOtherDiv.style.display = "block";
        }

        // 🔥 CLEAR HIDDEN VALUES
        if (outcomeDateDiv && outcomeDateDiv.style.display === "none") {
            const field = document.getElementById("id_outcome_date");
            if (field) field.value = "";
        }

        if (outcomeOtherDiv && outcomeOtherDiv.style.display === "none") {
            const field = document.getElementById("id_outcome_other");
            if (field) field.value = "";
        }
    }

    // INITIAL
    toggleOutcomeFields();

    // EVENT
    if (outcomeField) {
        outcomeField.addEventListener("change", toggleOutcomeFields);
    }

});