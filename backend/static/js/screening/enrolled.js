document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // FIELDS
    // =========================
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

    const enrolled = document.getElementById("id_enrolled");
    const reason = document.getElementById("id_reason");
    const reasonOther = document.getElementById("id_reason_other");

    const enrolledWrapper = document.getElementById("enrolled-wrapper");
    const reasonWrapper = document.getElementById("reason-wrapper");
    const reasonOtherWrapper = document.getElementById("reason-other-wrapper");

    const sex = document.getElementById("subject-sex")?.value;

    // =========================
    // HELPERS
    // =========================
    function isYes(field) {
        return String(field?.value || "") === "1";
    }

    function isNo(field) {
        return String(field?.value || "") === "2";
    }

    // =========================
    // TOGGLE FUNCTION 🔥
    // =========================
    function toggleEnrollment() {

        let showEnrolled = false;
        let showReason = false;
        let showReasonOther = false;

        // =========================
        // ELIGIBILITY LOGIC
        // =========================
        const basic =
            isYes(consent) &&
            isYes(age) &&
            isYes(biopsy);

        let hasCancer = false;

        if (sex === "1") {
            hasCancer = isYes(breast) || isYes(brain) || isYes(prostate);
        } else if (sex === "2") {
            hasCancer = isYes(breast) || isYes(brain) || isYes(cervical);
        }

        let hasExclusion =
            isYes(ckd) ||
            isYes(liver);

        if (sex === "2") {
            hasExclusion =
                hasExclusion ||
                isYes(pregnant) ||
                isYes(breastfeeding);
        }

        const eligible = basic && hasCancer && !hasExclusion;

        // =========================
        // ENROLLED
        // =========================
        if (eligible) {
            showEnrolled = true;
        } else {
            enrolled.value = "";
            reason.value = "";
            reasonOther.value = "";
        }

        // =========================
        // REASON
        // =========================
        if (isNo(enrolled)) {
            showReason = true;
        }

        // =========================
        // REASON OTHER
        // =========================
        if (reason && reason.value === "96") {
            showReasonOther = true;
        } else {
            reasonOther.value = "";
        }

        // =========================
        // APPLY UI
        // =========================
        enrolledWrapper.style.display = showEnrolled ? "block" : "none";
        reasonWrapper.style.display = showReason ? "block" : "none";
        reasonOtherWrapper.style.display = showReasonOther ? "block" : "none";
    }

    // =========================
    // INITIAL RUN
    // =========================
    toggleEnrollment();

    // =========================
    // EVENTS
    // =========================
    [
        consent, age, biopsy,
        breast, brain, cervical, prostate,
        ckd, liver, pregnant, breastfeeding,
        enrolled, reason
    ].forEach(field => {
        field?.addEventListener("change", toggleEnrollment);
    });

});