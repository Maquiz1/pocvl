document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // GET FIELDS
    // =========================
    const reasonField = document.getElementById("id_reason");
    const withdrewReasonField = document.getElementById("id_withdrew_reason");
    const outcomeField = document.getElementById("id_outcome");

    // =========================
    // GET CONTAINERS (IMPORTANT)
    // wrap inputs in divs with these IDs in template
    // =========================
    const reasonOtherDiv = document.getElementById("div_reason_other");
    const withdrewDiv = document.getElementById("div_withdrew_reason");
    const withdrewOtherDiv = document.getElementById("div_withdrew_other");
    const deathDiv = document.getElementById("div_death_fields");
    const outcomeOtherDiv = document.getElementById("div_outcome_other");

    // =========================
    // HELPER: GET SELECT TEXT
    // =========================
    function getSelectedText(select) {
        if (!select) return "";
        return select.options[select.selectedIndex]?.text.toUpperCase() || "";
    }

    // =========================
    // TOGGLE REASON-BASED FIELDS
    // =========================
    function toggleReasonFields() {

        const selectedText = getSelectedText(reasonField);

        // RESET ALL
        if (reasonOtherDiv) reasonOtherDiv.style.display = "none";
        if (withdrewDiv) withdrewDiv.style.display = "none";
        if (withdrewOtherDiv) withdrewOtherDiv.style.display = "none";
        if (deathDiv) deathDiv.style.display = "none";

        // =====================
        // WITHDRAW
        // =====================
        if (selectedText.includes("WITHDRAW")) {
            if (withdrewDiv) withdrewDiv.style.display = "block";
        }

        // =====================
        // DEATH
        // =====================
        if (selectedText.includes("DEATH")) {
            if (deathDiv) deathDiv.style.display = "block";
        }

        // =====================
        // OTHER
        // =====================
        if (selectedText.includes("OTHER")) {
            if (reasonOtherDiv) reasonOtherDiv.style.display = "block";
        }
    }

    // =========================
    // TOGGLE WITHDRAW OTHER
    // =========================
    function toggleWithdrewOther() {
        const selectedText = getSelectedText(withdrewReasonField);

        if (withdrewOtherDiv) {
            if (selectedText.includes("OTHER")) {
                withdrewOtherDiv.style.display = "block";
            } else {
                withdrewOtherDiv.style.display = "none";
            }
        }
    }

    // =========================
    // TOGGLE OUTCOME OTHER
    // =========================
    function toggleOutcomeOther() {
        const selectedText = getSelectedText(outcomeField);

        if (outcomeOtherDiv) {
            if (selectedText.includes("OTHER")) {
                outcomeOtherDiv.style.display = "block";
            } else {
                outcomeOtherDiv.style.display = "none";
            }
        }
    }

    // =========================
    // INITIAL RUN
    // =========================
    toggleReasonFields();
    toggleWithdrewOther();
    toggleOutcomeOther();

    // =========================
    // EVENTS
    // =========================
    if (reasonField) {
        reasonField.addEventListener("change", toggleReasonFields);
    }

    if (withdrewReasonField) {
        withdrewReasonField.addEventListener("change", toggleWithdrewOther);
    }

    if (outcomeField) {
        outcomeField.addEventListener("change", toggleOutcomeOther);
    }

});