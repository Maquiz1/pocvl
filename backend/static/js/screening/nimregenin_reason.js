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

    function isOther(val) {
        return val === "16";  // NO
    }

    // =========================
    // NIMREGENIN DATE + REASONS
    // =========================
    function toggleNimregeninOtherFields() {

        const val = $("#id_nimregenin_reasons").val();

        // ✅ Show reasons if NO
        if (isOther(val)) {
            $("#nimregenin-other-wrapper").show();
        } else {
            $("#nimregenin-other-wrapper").hide();
            // optional reset:
            // $("#id_nimregenin_reasons").val("");
        }
    }

    // =========================
    // EVENTS
    // =========================
    $("#id_nimregenin_reasons").on("change", toggleNimregeninOtherFields);

    // =========================
    // INITIAL LOAD
    // =========================
    toggleNimregeninOtherFields();

});