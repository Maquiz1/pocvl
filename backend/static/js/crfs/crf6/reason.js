document.addEventListener("DOMContentLoaded", function () {

    const reasonField = document.getElementById("id_reason");

    const reasonDateDiv = document.getElementById("div_reason_date_fields");
    const reasonOtherDiv = document.getElementById("div_reason_other");

    const withdrawSection = document.getElementById("div_withdraw_section");
    const deathFields = document.getElementById("div_death_fields");

    function toggleReasonFields() {

        if (!reasonField) return;

        const value = reasonField.value;

        // =========================
        // RESET ALL FIRST
        // =========================
        if (reasonDateDiv) reasonDateDiv.style.display = "none";
        if (reasonOtherDiv) reasonOtherDiv.style.display = "none";
        if (withdrawSection) withdrawSection.style.display = "none";
        if (deathFields) deathFields.style.display = "none";

        // =========================
        // 1–5 → SHOW REASON DATE
        // =========================
        if (["1", "2", "3", "4", "5"].includes(value)) {
            if (reasonDateDiv) reasonDateDiv.style.display = "block";
        }

        // =========================
        // 7 → SHOW OTHER
        // =========================
        if (value === "7") {
            if (reasonOtherDiv) reasonOtherDiv.style.display = "block";
        }

        // =========================
        // 3 → SHOW WITHDRAW SECTION
        // =========================
        if (value === "3") {
            if (withdrawSection) withdrawSection.style.display = "flex"; // row layout
        }

        // =========================
        // 2 → SHOW DEATH FIELDS
        // =========================
        if (value === "2") {
            if (deathFields) deathFields.style.display = "flex";
        }

        // =========================
        // 🔥 OPTIONAL: CLEAR HIDDEN VALUES (VERY IMPORTANT)
        // =========================
        if (reasonDateDiv && reasonDateDiv.style.display === "none") {
            const field = document.getElementById("id_reason_date");
            if (field) field.value = "";
        }

        if (reasonOtherDiv && reasonOtherDiv.style.display === "none") {
            const field = document.getElementById("id_reason_other");
            if (field) field.value = "";
        }

        if (withdrawSection && withdrawSection.style.display === "none") {
            const f1 = document.getElementById("id_withdrew_reason");
            const f2 = document.getElementById("id_withdrew_other");
            if (f1) f1.value = "";
            if (f2) f2.value = "";
        }

        if (deathFields && deathFields.style.display === "none") {
            const f1 = document.getElementById("id_primary_cause");
            const f2 = document.getElementById("id_secondary_cause");
            if (f1) f1.value = "";
            if (f2) f2.value = "";
        }
    }

    // =========================
    // INITIAL LOAD
    // =========================
    toggleReasonFields();

    // =========================
    // EVENT LISTENER
    // =========================
    if (reasonField) {
        reasonField.addEventListener("change", toggleReasonFields);
    }

});