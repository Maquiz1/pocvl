document.addEventListener("DOMContentLoaded", function () {

    const RadiotherapyPerformed = document.getElementById("id_radiotherapy_performed");
    const tableCard = document.getElementById("radio-table");
    const addBtn = document.getElementById("add-radio");
    const tbody = document.getElementById("radio-body");
    const totalForms = document.getElementById("id_radiotherapies-TOTAL_FORMS");

    // =========================
    // SHOW / HIDE TABLE
    // =========================

    function toggleTable() {
        const valText = RadiotherapyPerformed.options[RadiotherapyPerformed.selectedIndex].text.toLowerCase();

        const hasRows = tbody.querySelectorAll(".radio-row:not([style*='display: none'])").length > 0;

        if (valText === "yes" || hasRows) {
            tableCard.style.display = "";
        } else {
            tableCard.style.display = "none";
        }

        // ✅ HERE
        addBtn.disabled = valText !== "yes";
    }

    RadiotherapyPerformed.addEventListener("change", toggleTable);
    toggleTable();

    // =========================
    // ADD ROW
    // =========================
    addBtn.addEventListener("click", function () {

        let formCount = parseInt(totalForms.value);

        let template = document.getElementById("radio-empty")?.innerHTML;

        if (!template) {
            console.error("Radiotherapy empty form template missing!");
            return;
        }

        template = template.replace(/__prefix__/g, formCount);

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

        if (e.target.classList.contains("remove-radio")) {

            const row = e.target.closest("tr");

            const deleteInput = row.querySelector("input[type='checkbox']");

            if (deleteInput) {
                // EXISTING ROW → soft delete
                deleteInput.checked = true;
                row.style.display = "none";
            } else {
                // NEW ROW → remove
                row.remove();
                totalForms.value = tbody.querySelectorAll(".radio-row").length;
            }

            toggleTable();
        }
    });

    // =========================
    // AUTO-HIDE END DATE (ONGOING = YES)
    // =========================
    tbody.addEventListener("change", function (e) {

        if (e.target.name.includes("radiotherapy_ongoing")) {

            const row = e.target.closest("tr");
            const endInput = row.querySelector("input[name*='radiotherapy_end']");

            if (!endInput) return;

            const isOngoingYes = e.target.value === "1";

            if (isOngoingYes) {
                endInput.value = "";
                endInput.closest("td").style.display = "none";
            } else {
                endInput.closest("td").style.display = "";
            }
        }
    });

    // =========================
    // INIT EXISTING ROWS (UPDATE MODE)
    // =========================
    function initExistingRows() {
        tbody.querySelectorAll(".radio-row").forEach(row => {

            const ongoingSelect = row.querySelector("select[name*='radiotherapy_ongoing']");
            const endInput = row.querySelector("input[name*='radiotherapy_end']");

            if (!ongoingSelect || !endInput) return;

            if (ongoingSelect.value === "1") {
                endInput.closest("td").style.display = "none";
            }
        });
    }

    initExistingRows();

    // =========================
    // PREVENT EMPTY ROWS
    // =========================
    document.querySelector("form").addEventListener("submit", function () {

        tbody.querySelectorAll(".radio-row").forEach(row => {

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