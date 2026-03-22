$(document).ready(function () {

    // =========================
    // HELPERS (FK SAFE)
    // =========================
    function isYes(val) {
        return val === "1";  // YES
    }

    function isNo(val) {
        return val === "2";  // NO
    }

    // =========================
    // NIMREGENIN DATE + REASONS
    // =========================
    function toggleNimrFields() {

        const val = $("#id_consent_nimregenin").val();

        // ✅ Show date if YES
        if (isYes(val)) {
            $("#nimregenin-date-wrapper").show();
        } else {
            $("#nimregenin-date-wrapper").hide();
            // optional reset:
            // $("#id_nimregenin_date").val("");
        }

        // ✅ Show reasons if NO
        if (isNo(val)) {
            $("#nimregenin-reasons-wrapper").show();
        } else {
            $("#nimregenin-reasons-wrapper").hide();
            // optional reset:
            // $("#id_nimregenin_reasons").val("");
        }

        // 🔥 UNKNOWN (3) → hide both
        if (val === "3" || !val) {
            $("#nimregenin-date-wrapper").hide();
            $("#nimregenin-reasons-wrapper").hide();
        }
    }

    // =========================
    // EVENTS
    // =========================
    $("#id_consent_nimregenin").on("change", toggleNimrFields);

    // =========================
    // INITIAL LOAD
    // =========================
    toggleNimrFields();

});