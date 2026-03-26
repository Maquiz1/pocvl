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

    function isOther(val) {
        return val === "16";
    }

    // =========================
    // CONSENT DATE + REASONS
    // =========================
    function toggleConsentReasonFields() {

        const val = $("#id_consent_reasons").val();

        // ✅ Show reasons if NO
        if (isOther(val)) {
            $("#consent-other-wrapper").show();
        } else {
            $("#consent-other-wrapper").hide();
            // optional reset:
            // $("#id_consent_reasons").val("");
        }
    }

    // =========================
    // EVENTS
    // =========================
    $("#id_consent_reasons").on("change", toggleConsentReasonFields);

    // =========================
    // INITIAL LOAD
    // =========================
    toggleConsentReasonFields();

});