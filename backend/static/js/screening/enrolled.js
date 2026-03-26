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
    const reasonDate = document.getElementById("id_reason_date");

    const enrolledHeaderWrapper = document.getElementById("enrolled-header-wrapper");
    const enrolledWrapper = document.getElementById("enrolled-wrapper");
    const reasonWrapper = document.getElementById("reason-wrapper");
    const reasonOtherWrapper = document.getElementById("reason-other-wrapper");
    const reasonDateWrapper = document.getElementById("reason-date-wrapper");

    const eligibilityBadge = document.getElementById("eligibility-badge");

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

    function resetField(field) {
        if (field) field.value = "";
    }

    function toggle(el, show) {
        if (!el) return;   // 🔥 prevents crash
        el.style.display = show ? "block" : "none";
    }

    function updateBadge(isEligible) {
        if (!eligibilityBadge) return;

        if (isEligible) {
            eligibilityBadge.className = "badge bg-success";
            eligibilityBadge.innerText = "Eligible";
        } else {
            eligibilityBadge.className = "badge bg-danger";
            eligibilityBadge.innerText = "Not Eligible";
        }
    }

    // =========================
    // MAIN LOGIC
    // =========================
    function toggleEnrollment() {

        let showEnrolledHeader = false;
        let showEnrolled = false;
        let showReason = false;
        let showReasonOther = false;
        let showReasonDate = false;

        // =========================
        // ELIGIBILITY
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

        // 🔥 UPDATE BADGE
        updateBadge(eligible);

        // 🔥 OPTIONAL: disable enrolled if not eligible
        if (enrolled) {
            enrolled.disabled = !eligible;
        }

        // =========================
        // ENROLLMENT (FIXED)
        // =========================
        const hasValue = enrolled && enrolled.value !== "";

        if (eligible || hasValue) {
            showEnrolledHeader = true;
            showEnrolled = true;
        } else {
            showEnrolledHeader = false;
            showEnrolled = false;

            resetField(enrolled);
            resetField(reason);
            resetField(reasonOther);
            resetField(reasonDate);
        }

        // =========================
        // REASON (FIXED)
        // =========================
        if (enrolled && enrolled.value === "2") {
            showReason = true;
        }

        // =========================
        // REASON OTHER
        // =========================
        if (reason && reason.value === "16") {
            showReasonOther = true;
        } else {
            resetField(reasonOther);
        }

        // =========================
        // REASON DATE
        // =========================
        if (reason && ["4", "5", "14", "15"].includes(reason.value)) {
            showReasonDate = true;
        } else {
            resetField(reasonDate);
        }

        // =========================
        // APPLY UI
        // =========================
        toggle(enrolledHeaderWrapper, showEnrolledHeader);
        toggle(enrolledWrapper, showEnrolled);
        toggle(reasonWrapper, showReason);
        toggle(reasonOtherWrapper, showReasonOther);
        toggle(reasonDateWrapper, showReasonDate);
    }

    // =========================
    // INIT
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