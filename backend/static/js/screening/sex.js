$(document).ready(function () {

    // =========================
    // SAFE SEX VALUE
    // =========================
    const sexVal = $("#subject-sex").val();
    const sex = sexVal ? parseInt(sexVal) : null; // 1=Male, 2=Female

    // =========================
    // HELPERS
    // =========================
    function clearField(selector) {
        $(selector).val("").trigger("change");
    }

    function hideAndClear(wrapper, field) {
        $(wrapper).hide();
        clearField(field);
    }

    // =========================
    // SEX-BASED LOGIC
    // =========================
    function handleSexUI() {

        if (sex === 1) { // 👨 Male

            // Hide female-only fields
            hideAndClear("#cervical-wrapper", "#id_cervical_cancer");
            hideAndClear("#pregnant-wrapper", "#id_pregnant");
            hideAndClear("#breastfeeding-wrapper", "#id_breast_feeding");

        } else if (sex === 2) { // 👩 Female

            // Hide male-only field
            hideAndClear("#prostate-wrapper", "#id_prostate_cancer");

        }
    }

    // =========================
    // INIT
    // =========================
    handleSexUI();

});