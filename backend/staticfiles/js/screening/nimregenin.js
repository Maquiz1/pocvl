$(document).ready(function () {

    const YES = "1";
    const NO = "2";

    // =========================
    // ✅ NIMREGENIN DATE + REASONS
    // =========================
    function toggleNimrFields() {
        const val = $("#id_consent_nimregenin").val();

        // ✅ Show date if YES
        if (val === YES) {
            $("#nimregenin-date-wrapper").show();
        } else {
            $("#nimregenin-date-wrapper").hide();
            // $("#id_nimregenin_date").val("");
        }

        // ✅ Show reasons if NO
        if (val === NO) {
            $("#nimregenin-reasons-wrapper").show();
        } else {
            $("#nimregenin-reasons-wrapper").hide();
            // $("#id_nimregenin_reasons").val("");
        }
    }

    $("#id_consent_nimregenin").on("change", toggleNimrFields);

    // Initial run
    toggleNimrFields();

});