document.addEventListener("DOMContentLoaded", function () {

    const otherMedical = document.getElementById("id_other_medical");
    const tableCard = document.getElementById("other-medical-table");
    const addBtn = document.getElementById("add-row");
    const tbody = document.getElementById("other-body");
    const totalForms = document.querySelector(
        "input[name='othermedicals-TOTAL_FORMS']"
    );
    const emptyForm = document.getElementById("other-empty-form");

    console.log({
        otherMedical,
        tableCard,
        addBtn,
        tbody,
        totalForms,
        emptyForm
    });

    // // 🔥 SAFETY CHECK
    if (!otherMedical || !tableCard || !addBtn || !tbody || !totalForms || !emptyForm) {
        console.error("❌ otherMedical setup failed");
        return;
    }
    

    function isYes(select) {
        if (!select) return false;
        return ["1", "yes", "true", "True"].includes(select.value);
    }
    // =========================
    // SHOW / HIDE TABLE
    // =========================
    function toggleTable() {
        const hasRows = tbody.querySelectorAll(
            ".other-row:not([style*='display: none'])"
        ).length > 0;

        if (isYes(otherMedical) || hasRows) {
            tableCard.style.display = "block"; // force visible
        } else {
            tableCard.style.display = "none";
        }

        addBtn.disabled = !isYes(otherMedical);
    }

    otherMedical.addEventListener("change", toggleTable);
    toggleTable();

    // =========================
    // ADD ROW
    // =========================
    addBtn.addEventListener("click", function () {

        let formCount = parseInt(totalForms.value);

        let template = emptyForm.innerHTML;

        if (!template) {
            console.error("Empty form template not found!");
            return;
        }

        // replace prefix
        template = template.replace(/__prefix__/g, formCount);

        // create element safely
        const tempDiv = document.createElement("tbody");
        tempDiv.innerHTML = template.trim();

        const newRow = tempDiv.firstElementChild;

        if (!newRow) {
            console.error("Failed to create new row");
            return;
        }

        tbody.appendChild(newRow);

        // increment TOTAL_FORMS
        totalForms.value = formCount + 1;

        console.log("TOTAL_FORMS:", totalForms.value);

        toggleTable();
    });

    // =========================
    // REMOVE ROW (SMART)
    // =========================
    tbody.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-row")) {

            const row = e.target.closest("tr");

            const deleteInput = row.querySelector("input[name$='-DELETE']");

            if (deleteInput) {
                // existing row → soft delete
                deleteInput.checked = true;
                row.style.display = "none";
            } else {
                // new row → remove only
                row.remove();
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