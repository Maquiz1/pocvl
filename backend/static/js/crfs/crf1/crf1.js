document.addEventListener("DOMContentLoaded", function () {

    function handleGroup(diseaseId, medClass, nameClass) {

        const disease = document.getElementById(`id_${diseaseId}`);
        const medWrapper = document.querySelector(`.${medClass}`);
        const nameWrapper = document.querySelector(`.${nameClass}`);

        if (!disease || !medWrapper || !nameWrapper) return;

        const med = medWrapper.querySelector("select");
        const name = nameWrapper.querySelector("input");

        function toggleFields() {

            if (disease.value === "1") {

                // Show medication field
                medWrapper.style.display = "block";

                if (med && med.value === "1") {
                    nameWrapper.style.display = "block";
                } else {
                    nameWrapper.style.display = "none";
                    if (name) name.value = "";
                }

            } else {
                // Hide everything
                medWrapper.style.display = "none";
                nameWrapper.style.display = "none";

                if (med) med.selectedIndex = 0;
                if (name) name.value = "";
            }
        }

        // Run on load
        toggleFields();

        // Run on change
        disease.addEventListener("change", toggleFields);
        if (med) med.addEventListener("change", toggleFields);
    }

    // Apply to all groups
    handleGroup("diabetic", "diabetic-med", "diabetic-name");
    handleGroup("hypertension", "hypertension-med", "hypertension-name");
    handleGroup("heart", "heart-med", "heart-name");
    handleGroup("asthma", "asthma-med", "asthma-name");
    handleGroup("hiv_aids", "hiv-med", "hiv-name");

});