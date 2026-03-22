$(document).ready(function () {

    // =========================
    // ✅ NEW TREATMENT LOGIC
    // =========================
    function handleNewTreatmentUI() {

        const treatment = parseInt($("#id_treatment_type").val());

        if ([1, 2, 3, 4, 5].includes(treatment)) {
            $("#new-date-wrapper").show();
            $("#new-other-wrapper").hide();
        }else if ([6].includes(treatment)) {
            $("#new-date-wrapper").show();
            $("#new-other-wrapper").show();
        } else {
            $("#new-date-wrapper").hide();
            // $("#id_treatment_date").val("");
            $("#new-other-wrapper").hide();
        }

        // if ([6].includes(treatment)) {
        //     $("#new-date-wrapper").show();
        //     $("#new-other-wrapper").show();
        // } else {
        //     $("#new-other-wrapper").hide();
        //     $("#new-date-wrapper").hide();
        //     // $("#id_treatment_date").val("");
        // }
    }

    // =========================
    // INIT
    // =========================
    handleNewTreatmentUI();

    // =========================
    // EVENTS
    // =========================

    $("#id_treatment_type").change(function () {
        handleNewTreatmentUI();
    });

});