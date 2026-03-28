document.addEventListener("DOMContentLoaded", function () {
    const local_examinationField = document.getElementById("id_local_examination");
    const local_examinationComments = document.getElementById("local_examination-comments");
    const local_examinationSignifcnt = document.getElementById("local_examination-signifcnt");

    function togglelocal_examinationFields() {
        if (local_examinationField.value === "2") {
            local_examinationComments.style.display = "table-cell";
            local_examinationSignifcnt.style.display = "table-cell";
        } else {
            local_examinationComments.style.display = "none";
            local_examinationSignifcnt.style.display = "none";
        }
    }

    // Run on load
    togglelocal_examinationFields();

    // Run on change
    local_examinationField.addEventListener("change", togglelocal_examinationFields);
});
