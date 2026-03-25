document.addEventListener("DOMContentLoaded", function () {

    const enrolledField = document.getElementById("id_enrolled");
    const reasonField = document.getElementById("id_reason");
    const reasonOtherField = document.getElementById("id_reason_other");

    const enrolledWrapper = document.getElementById("enrolled-wrapper");
    const reasonWrapper = document.getElementById("reason-wrapper");
    const reasonOtherWrapper = document.getElementById("reason-other-wrapper");

    const sex = document.getElementById("subject-sex")?.value;

    // =========================
    // HELPERS
    // =========================
    function isYes(select) {
        if (!select || !select.value) return false;
        return select.options[select.selectedIndex].text.toLowerCase() === "yes";
    }

    function isNo(select) {
        if (!select || !select.value) return false;
        return select.options[select.selectedIndex].text.toLowerCase() === "no";
    }

    // =========================
    // SEX UI CONTROL
    // =========================
    if (sex == "1") {
        document.getElementById("id_cervical_cancer")?.closest(".col-md-3").style.display = "none";
        document.getElementById("id_pregnant")?.closest(".col-md-3").style.display = "none";
        document.getElementById("id_breast_feeding")?.closest(".col-md-3").style.display = "none";
    }

    if (sex == "2") {
        document.getElementById("id_prostate_cancer")?.closest(".col-md-3").style.display = "none";
    }

    // =========================
    // COMPUTE ELIGIBILITY (FINAL ✅)
    // =========================
    function computeEligible() {

        const consent = document.getElementById("id_consent");
        const age = document.getElementById("id_age_18");
        const biopsy = document.getElementById("id_biopsy");

        const breast = document.getElementById("id_breast_cancer");
        const brain = document.getElementById("id_brain_cancer");
        const cervical = document.getElementById("id_cervical_cancer");
        const prostate = document.getElementById("id_prostate_cancer");

        const ckd = document.getElementById("id_ckd");
        const liver = document.getElementById("id_liver_disease");
        const pregnant = document.getElementById("id_pregnant");
        const breastfeeding = document.getElementById("id_breast_feeding");

        const basic =
            isYes(consent) &&
            isYes(age) &&
            isYes(biopsy);

        let hasCancer = false;

        if (sex == "1") {
            hasCancer =
                isYes(breast) ||
                isYes(brain) ||
                isYes(prostate);
        } else if (sex == "2") {
            hasCancer =
                isYes(breast) ||
                isYes(brain) ||
                isYes(cervical);
        }

        let hasExclusion =
            isYes(ckd) ||
            isYes(liver);

        if (sex == "2") {
            hasExclusion =
                hasExclusion ||
                isYes(pregnant) ||
                isYes(breastfeeding);
        }

        return basic && hasCancer && !hasExclusion;
    }

    // =========================
    // MAIN UI LOGIC 🔥
    // =========================
    function toggleEnrollment() {

        const eligible = computeEligible();

        // Show enrolled only if eligible
        if (eligible) {
            enrolledWrapper.style.display = "";
        } else {
            enrolledWrapper.style.display = "none";

            enrolledField.value = "";
            reasonField.value = "";
            reasonOtherField.value = "";
        }

        if (!enrolledField.value) {
            reasonWrapper.style.display = "none";
            reasonOtherWrapper.style.display = "none";
            return;
        }

        if (isYes(enrolledField)) {
            reasonWrapper.style.display = "none";
            reasonOtherWrapper.style.display = "none";

            reasonField.value = "";
            reasonOtherField.value = "";
        }

        else if (isNo(enrolledField)) {
            reasonWrapper.style.display = "";
        }

        // =========================
        // REASON LOGIC
        // =========================
        if (!reasonField.value) {
            reasonOtherWrapper.style.display = "none";
            return;
        }

        const selectedOption = reasonField.options[reasonField.selectedIndex];
        const reasonCode = selectedOption?.dataset?.code || selectedOption?.value;

        if (reasonCode == "96") {
            reasonOtherWrapper.style.display = "";
        } else {
            reasonOtherWrapper.style.display = "none";
            reasonOtherField.value = "";
        }
    }

    // =========================
    // EVENTS
    // =========================
    [
        "id_consent",
        "id_age_18",
        "id_biopsy",
        "id_breast_cancer",
        "id_brain_cancer",
        "id_cervical_cancer",
        "id_prostate_cancer",
        "id_ckd",
        "id_liver_disease",
        "id_pregnant",
        "id_breast_feeding"
    ].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.addEventListener("change", toggleEnrollment);
    });

    enrolledField?.addEventListener("change", toggleEnrollment);
    reasonField?.addEventListener("change", toggleEnrollment);

    // initial run
    toggleEnrollment();

});