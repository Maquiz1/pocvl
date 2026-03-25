document.addEventListener("DOMContentLoaded", function () {

    const field = document.getElementById("id_physical_exams_other");
    const section = document.getElementById("other-exams-section");

    const addBtn = document.getElementById("add-row");
    const formsetBody = document.getElementById("formset-body");
    const totalForms = document.getElementById("id_other_physcl_exams-TOTAL_FORMS");

    if (!totalForms) {
        console.error("TOTAL_FORMS not found — check prefix!");
        return;
    }

    // 🔥 SHOW / HIDE SECTION
    function toggleSection() {
        if (field.value === "1") {
            section.style.display = "block";
        } else {
            section.style.display = "none";
        }
    }

    // run on load
    toggleSection();

    // run on change
    field.addEventListener("change", toggleSection);

    // 🔥 ADD ROW
    addBtn.addEventListener("click", function () {
        const formCount = parseInt(totalForms.value);

        const firstRow = document.querySelector(".formset-row");
        const newRow = firstRow.cloneNode(true);

        newRow.querySelectorAll("input, select, textarea").forEach(function (el) {
            if (el.name) {
                el.name = el.name.replace(/-\d+-/, `-${formCount}-`);
            }
            if (el.id) {
                el.id = el.id.replace(/-\d+-/, `-${formCount}-`);
            }

            if (el.type !== "hidden") {
                el.value = "";
            }
        });

        formsetBody.appendChild(newRow);
        totalForms.value = formCount + 1;
    });

    // 🔥 REMOVE ROW (proper delete)
    document.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-row")) {
            const row = e.target.closest(".formset-row");
            const deleteInput = row.querySelector("input[type='checkbox']");

            if (deleteInput) {
                deleteInput.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
            }
        }
    });

});
