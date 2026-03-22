$(document).ready(function () {

    const YES = "1";
    const NO = "2";

    // =========================
    // ✅ CONSENT DATE + REASONS
    // =========================
    function toggleConsentFields() {
        const val = $("#id_consent").val();

        // ✅ Show date if YES
        if (val === YES) {
            $("#consent-date-wrapper").show();
        } else {
            $("#consent-date-wrapper").hide();
            // $("#id_consent_date").val("");
        }

        // ✅ Show reasons if NO
        if (val === NO) {
            $("#consent-reasons-wrapper").show();
        } else {
            $("#consent-reasons-wrapper").hide();
            // $("#id_consent_reasons").val("");
        }
    }

    $("#id_consent").on("change", toggleConsentFields);

    // Initial run
    toggleConsentFields();

});