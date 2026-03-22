$(document).ready(function () {

    // =========================
    // ✅ PREVIOUS TREATMENT LOGIC
    // =========================
    function handlePreviousTreatmentUI() {

        const prevTreatment = parseInt($("#id_previous_treatment").val());

        if ([1, 2, 3, 4, 5].includes(prevTreatment)) {
            $("#previous-date-wrapper").show();
            $("#previous-other-wrapper").hide();
        }else if ([6].includes(prevTreatment)) {
            $("#previous-date-wrapper").show();
            $("#previous-other-wrapper").show();
        } else {
            $("#previous-date-wrapper").hide();
            // $("#id_previous_date").val("");
            $("#previous-other-wrapper").hide();
        }
    }

    // =========================
    // INIT
    // =========================
    handlePreviousTreatmentUI();

    // =========================
    // EVENTS
    // =========================

    $("#id_previous_treatment").change(function () {
        handlePreviousTreatmentUI();
    });

});