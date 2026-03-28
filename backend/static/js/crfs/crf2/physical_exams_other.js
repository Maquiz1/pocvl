document.addEventListener("DOMContentLoaded", function () {
    const physical_exams_otherField = document.getElementById("id_physical_exams_other");
    const physical_exams_otherComments = document.getElementById("physical_exams_other-comments");
    const physical_exams_otherSignifcnt = document.getElementById("physical_exams_other-signifcnt");

    function togglephysical_exams_otherFields() {
        if (physical_exams_otherField.value === "2") {
            physical_exams_otherComments.style.display = "table-cell";
            physical_exams_otherSignifcnt.style.display = "table-cell";
        } else {
            physical_exams_otherComments.style.display = "none";
            physical_exams_otherSignifcnt.style.display = "none";
        }
    }

    // Run on load
    togglephysical_exams_otherFields();

    // Run on change
    physical_exams_otherField.addEventListener("change", togglephysical_exams_otherFields);
});
