document.addEventListener("DOMContentLoaded", function () {

    const otherMedical = document.getElementById("id_other_medical");
    const tableCard = document.getElementById("other-medical-table");
    const addBtn = document.getElementById("add-row");
    const tbody = document.getElementById("other-body");
    const totalForms = document.getElementById("id_othermedical-TOTAL_FORMS");

    // =========================
    // SHOW / HIDE TABLE
    // =========================
    function toggleTable() {
        const valText = otherMedical.options[otherMedical.selectedIndex].text.toLowerCase();

        const hasRows = tbody.querySelectorAll(".other-row:not([style*='display: none'])").length > 0;

        if (valText === "yes" || hasRows) {
            tableCard.style.display = "";
        } else {
            tableCard.style.display = "none";
        }

        // ✅ HERE
        addBtn.disabled = valText !== "yes";
    }

    otherMedical.addEventListener("change", toggleTable);
    toggleTable();

    // =========================
    // ADD ROW
    // =========================
    addBtn.addEventListener("click", function () {

        let formCount = parseInt(totalForms.value);

        let template = document.getElementById("other-empty-form")?.innerHTML;

        if (!template) {
            console.error("Empty form template not found!");
            return;
        }

        // 🔥 CRITICAL FIX
        template = template.replace(/__prefix__/g, formCount);

        // 🔥 FORCE HTML parsing correctly
        const tempDiv = document.createElement("tbody");
        tempDiv.innerHTML = template;

        tbody.appendChild(tempDiv.firstElementChild);

        totalForms.value = formCount + 1;

        toggleTable();
    });

    // =========================
    // REMOVE ROW (SMART)
    // =========================
    tbody.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-row")) {

            const row = e.target.closest("tr");

            // 🔥 check if existing form (has DELETE checkbox)
            const deleteInput = row.querySelector("input[type='checkbox']");

            if (deleteInput) {
                // EXISTING ROW → soft delete
                deleteInput.checked = true;
                row.style.display = "none";
            } else {
                // NEW ROW → remove from DOM
                row.remove();

                // update TOTAL_FORMS
                totalForms.value = tbody.querySelectorAll(".other-row").length;
            }

            toggleTable();
        }
    });

    // =========================
    // PREVENT EMPTY ROWS
    // =========================
    document.querySelector("form").addEventListener("submit", function () {

        document.querySelectorAll(".other-row").forEach(row => {

            const inputs = row.querySelectorAll("input, select, textarea");

            let hasValue = false;

            inputs.forEach(input => {
                if (input.type !== "checkbox" && input.value.trim() !== "") {
                    hasValue = true;
                }
            });

            // if empty → mark delete
            if (!hasValue) {
                const del = row.querySelector("input[type='checkbox']");
                if (del) del.checked = true;
            }
        });
    });

});