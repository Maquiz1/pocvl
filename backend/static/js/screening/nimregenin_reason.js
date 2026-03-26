$(document).ready(function () {

    function isOther(val) {
        return String(val) === "16";
    }

    function toggleNimregeninOtherFields() {

        const val = $("#id_nimregenin_reasons").val();

        if (isOther(val)) {
            $("#nimregenin-other-wrapper").show();
        } else {
            $("#nimregenin-other-wrapper").hide();
            // $("#id_nimregenin_other").val("");
        }
    }

    $("#id_nimregenin_reasons").on("change", toggleNimregeninOtherFields);

    toggleNimregeninOtherFields();
});