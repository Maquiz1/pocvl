$(document).ready(function () {

    const sex = parseInt($("#subject-sex").val()); // 1=Male, 2=Female

    // =========================
    // ✅ SEX-BASED LOGIC
    // =========================
    function handleSexUI() {

        if (sex === 1) { // 👨 Male

            // Hide female-only fields
            $("#cervical-wrapper").hide();
            $("#pregnant-wrapper").hide();
            $("#breastfeeding-wrapper").hide();

            // Clear values (IMPORTANT → backend will set NULL)
            $("#id_cervical_cancer").val("").trigger("change");
            $("#id_pregnant").val("").trigger("change");
            $("#id_breast_feeding").val("").trigger("change");

        } else if (sex === 2) { // 👩 Female

            // Hide male-only field
            $("#prostate-wrapper").hide();

            // Clear value
            $("#id_prostate_cancer").val("").trigger("change");
        }
    }

    handleSexUI();

});