document.addEventListener("DOMContentLoaded", function () {

    const radioPerformed = document.getElementById("id_radiotherapy_performed");
    const tableCard = document.getElementById("radio-table");
    const addBtn = document.getElementById("add-radio");
    const tbody = document.getElementById("radio-body");
    const totalForms = document.querySelector("input[name='radiotherapies-TOTAL_FORMS']");
    const emptyForm = document.getElementById("radio-empty-form");

    // console.log({
    //     radioPerformed,
    //     tableCard,
    //     addBtn,
    //     tbody,
    //     totalForms,
    //     emptyForm
    // });

    // 🔥 SAFETY CHECK
    if (!radioPerformed || !tableCard || !addBtn || !tbody || !totalForms || !emptyForm) {
        console.error("❌ Radiotherapy setup failed");
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
        const hasRows = tbody.querySelectorAll(".radio-row:not([style*='display: none'])").length > 0;

        if (isYes(radioPerformed) || hasRows) {
            tableCard.style.display = "block";
        } else {
            tableCard.style.display = "none";
        }

        addBtn.disabled = !isYes(radioPerformed);
    }

    radioPerformed.addEventListener("change", toggleTable);
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
        if (e.target.classList.contains("remove-radio")) {
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
    // AUTO-HIDE END DATE (ONGOING = YES)
    // =========================
    tbody.addEventListener("change", function (e) {
        if (e.target.name.includes("radiotherapy_ongoing")) {
            const row = e.target.closest("tr");
            const endInput = row.querySelector("input[name*='radiotherapy_end']");
            if (!endInput) return;

            const isOngoingYes = ["1", "yes", "true", "True"].includes(e.target.value);
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

            if (["1", "yes", "true", "True"].includes(ongoingSelect.value)) {
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
