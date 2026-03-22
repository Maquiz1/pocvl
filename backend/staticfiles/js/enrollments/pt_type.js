$(document).ready(function () {

    function handlePtTypeUI() {

        const ptType = parseInt($("#id_pt_type").val());

        // Hide all first
        $("#new-section").hide();
        $("#previous-section").hide();
        $("#cycle-section").hide();

        if (ptType === 1) {
            // ✅ New + Cycles
            $("#new-section").show();
            $("#cycle-section").show();

        } else if (ptType === 2) {
            // ✅ Previous + Cycles
            $("#previous-section").show();
            $("#cycle-section").show();

        } else if (ptType === 3) {
            // ✅ Hide everything
            $("#new-section").hide();
            $("#previous-section").hide();
            $("#cycle-section").hide();

            // // OPTIONAL: clear values (recommended)
            // $("#id_treatment_type").val("").trigger("change");
            // $("#id_treatment_date").val("");
            // $("#id_previous_treatment").val("").trigger("change");
            // $("#id_previous_date").val("");
            // $("#id_total_cycle").val("");
            // $("#id_cycle_number").val("");
        }
    }

    // Run on load
    handlePtTypeUI();

    // Run on change
    $("#id_pt_type").change(function () {
        handlePtTypeUI();
    });

});