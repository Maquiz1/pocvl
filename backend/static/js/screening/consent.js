$(document).ready(function () {

    // =========================
    // HELPERS (SAFE FK HANDLING)
    // =========================
    function isYes(val) {
        return val === "1";
    }

    function isNo(val) {
        return val === "2";
    }

    // =========================
    // CONSENT DATE + REASONS
    // =========================
    function toggleConsentFields() {

        const val = $("#id_consent").val();

        // ✅ Show date if YES
        if (isYes(val)) {
            $("#consent-date-wrapper").show();
        } else {
            $("#consent-date-wrapper").hide();
            // optional reset:
            // $("#id_consent_date").val("");
        }

        // ✅ Show reasons if NO
        if (isNo(val)) {
            $("#consent-reasons-wrapper").show();
        } else {
            $("#consent-reasons-wrapper").hide();
            // optional reset:
            // $("#id_consent_reasons").val("");
        }
    }

    // =========================
    // EVENTS
    // =========================
    $("#id_consent").on("change", toggleConsentFields);

    // =========================
    // INITIAL LOAD
    // =========================
    toggleConsentFields();

});