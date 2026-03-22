document.addEventListener("DOMContentLoaded", function () {
    // Result fields
    const Occupation = document.getElementById("id_occupation");

    // Field to show/hide
    const otherOccupationWrapper = document.getElementById("other-occupation-wrapper");

    function toggleOccupation() {

        const value = String(Occupation?.value || "");

        if (value === "3") {
            otherOccupationWrapper.style.display = "block";
        } else {
            otherOccupationWrapper.style.display = "none";
        }
    }

    // Initial state on page load
    toggleOccupation();

    // Update when either result changes
    Occupation.addEventListener("change", toggleOccupation);
});
