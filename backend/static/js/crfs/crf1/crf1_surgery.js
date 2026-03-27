document.addEventListener("DOMContentLoaded", function () {

    const surgeryPerformed = document.getElementById("id_surgery_performed");
    const tableCard = document.getElementById("surgery-table");
    const addBtn = document.getElementById("add-surgery");
    const tbody = document.getElementById("surgery-body");
    const totalForms = document.querySelector("input[name='surgeries-TOTAL_FORMS']");
    const emptyForm = document.getElementById("surgery-empty-form");

    // console.log({
    //     surgeryPerformed,
    //     tableCard,
    //     addBtn,
    //     tbody,
    //     totalForms,
    //     emptyForm
    // });

    // 🔥 SAFETY CHECK
    if (!surgeryPerformed || !tableCard || !addBtn || !tbody || !totalForms || !emptyForm) {
        console.error("❌ Surgery setup failed");
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
        const hasRows = tbody.querySelectorAll(".surgery-row:not([style*='display: none'])").length > 0;

        if (isYes(surgeryPerformed) || hasRows) {
            tableCard.style.display = "block";
        } else {
            tableCard.style.display = "none";
        }

        addBtn.disabled = !isYes(surgeryPerformed);
    }

    surgeryPerformed.addEventListener("change", toggleTable);
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

        template = template.replace(/__prefix__/g, formCount);

        const tempDiv = document.createElement("tbody");
        tempDiv.innerHTML = template.trim();

        const newRow = tempDiv.firstElementChild;
        if (!newRow) {
            console.error("Failed to create new row");
            return;
        }

        tbody.appendChild(newRow);
        totalForms.value = formCount + 1;

        toggleTable();
    });

    // =========================
    // REMOVE ROW (SMART)
    // =========================
    tbody.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-surgery")) {
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
        tbody.querySelectorAll(".surgery-row").forEach(row => {
            const inputs = row.querySelectorAll("input, select, textarea");
            let hasValue = false;

            inputs.forEach(input => {
                if (input.type !== "checkbox" && input.value.trim() !== "") {
                    hasValue = true;
                }
            });

            if (!hasValue) {
                const del = row.querySelector("input[type='checkbox']");
                if (del) del.checked = true;
            }
        });
    });

});
