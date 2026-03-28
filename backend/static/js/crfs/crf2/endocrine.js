document.addEventListener("DOMContentLoaded", function () {
    const endocrineField = document.getElementById("id_endocrine");
    const endocrineComments = document.getElementById("endocrine-comments");
    const endocrineSignifcnt = document.getElementById("endocrine-signifcnt");

    function toggleendocrineFields() {
        if (endocrineField.value === "2") {
            endocrineComments.style.display = "table-cell";
            endocrineSignifcnt.style.display = "table-cell";
        } else {
            endocrineComments.style.display = "none";
            endocrineSignifcnt.style.display = "none";
        }
    }

    // Run on load
    toggleendocrineFields();

    // Run on change
    endocrineField.addEventListener("change", toggleendocrineFields);
});
