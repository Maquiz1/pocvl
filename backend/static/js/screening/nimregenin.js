$(document).ready(function () {

    function isYes(val) { return String(val) === "1"; }
    function isNo(val) { return String(val) === "2"; }

    function toggleNimrFields() {

        const val = $("#id_consent_nimregenin").val();

        // DATE
        if (isYes(val)) {
            $("#nimregenin-date-wrapper").show();
        } else {
            $("#nimregenin-date-wrapper").hide();
            $("#id_nimregenin_date").val("");
        }

        // REASONS
        if (isNo(val)) {
            $("#nimregenin-reasons-wrapper").show();
        } else {
            $("#nimregenin-reasons-wrapper").hide();
            $("#id_nimregenin_reasons").val("");

            // 🔥 IMPORTANT: also reset OTHER
            $("#nimregenin-other-wrapper").hide();
            $("#id_nimregenin_other").val("");
        }

        // UNKNOWN
        if (val === "3" || !val) {
            $("#nimregenin-date-wrapper").hide();
            $("#nimregenin-reasons-wrapper").hide();
        }
    }

    $("#id_consent_nimregenin").on("change", toggleNimrFields);

    toggleNimrFields();
});