document.addEventListener("DOMContentLoaded", function () {

    function getText(select) {
        return select?.options[select.selectedIndex]?.text?.toLowerCase() || "";
    }

    function isYes(select) {
        return getText(select) === "yes";
    }

    function isNo(select) {
        return getText(select) === "no";
    }

    function isUnknown(select) {
        return getText(select) === "unknown";
    }

    function clearField(field) {
        if (!field) return;
        if (field.tagName === "SELECT") {
            field.selectedIndex = 0;
        } else {
            field.value = "";
        }
    }

    function handleGroup(diseaseId, medClass, nameClass) {

        const disease = document.getElementById(`id_${diseaseId}`);
        const medWrapper = document.querySelector(`.${medClass}`);
        const nameWrapper = document.querySelector(`.${nameClass}`);

        const med = medWrapper?.querySelector("select");
        const name = nameWrapper?.querySelector("input");

        function update() {
            const diseaseVal = getText(disease);

            // =========================
            // Disease = YES
            // =========================
            if (diseaseVal === "yes") {

                medWrapper.style.display = "";
                
                // Medication logic
                if (isYes(med)) {
                    nameWrapper.style.display = "";
                } else {
                    nameWrapper.style.display = "none";
                    clearField(name);
                }

            } else {
                // =========================
                // Disease = NO or UNKNOWN
                // =========================
                medWrapper.style.display = "none";
                nameWrapper.style.display = "none";

                clearField(med);
                clearField(name);
            }
        }

        // Events
        disease.addEventListener("change", update);
        med?.addEventListener("change", update);

        // Init
        update();
    }

    // =========================
    // APPLY TO ALL GROUPS
    // =========================

    handleGroup("diabetic", "diabetic-med", "diabetic-name");
    handleGroup("hypertension", "hypertension-med", "hypertension-name");
    handleGroup("heart", "heart-med", "heart-name");
    handleGroup("asthma", "asthma-med", "asthma-name");
    handleGroup("hiv_aids", "hiv-med", "hiv-name");

});