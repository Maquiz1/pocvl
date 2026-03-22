document.addEventListener("DOMContentLoaded", function () {

    function setupDynamicFormset(config) {

        const select = document.querySelector(`[name='${config.selectName}']`);
        const tableCard = document.getElementById(config.tableId);
        const addBtn = document.getElementById(config.addBtnId);
        const tbody = document.getElementById(config.tbodyId);
        const totalForms = document.getElementById(config.totalFormsId);
        const emptyForm = document.getElementById(config.emptyFormId);

        // 🚨 safety checks
        if (!select || !tableCard || !addBtn || !tbody || !totalForms || !emptyForm) {
            console.error("❌ Formset config error:", config);
            return;
        }

        // =========================
        // TOGGLE TABLE
        // =========================
        function toggleTable() {

            const value = select.value;

            const hasRows = tbody.querySelectorAll(
                `.${config.rowClass}:not([style*='display: none'])`
            ).length > 0;

            if (value === config.yesValue || hasRows) {
                tableCard.style.display = "";
            } else {
                tableCard.style.display = "none";
            }

            addBtn.disabled = value !== config.yesValue;
        }

        select.addEventListener("change", toggleTable);
        toggleTable();

        // =========================
        // ADD ROW
        // =========================
        addBtn.addEventListener("click", function () {

            let count = parseInt(totalForms.value);

            let template = emptyForm.innerHTML.replace(/__prefix__/g, count);

            const temp = document.createElement("tbody");
            temp.innerHTML = template;

            tbody.appendChild(temp.firstElementChild);

            totalForms.value = count + 1;

            toggleTable();
        });

        // =========================
        // REMOVE ROW
        // =========================
        tbody.addEventListener("click", function (e) {

            if (e.target.classList.contains(config.removeBtnClass)) {

                const row = e.target.closest("tr");
                const del = row.querySelector("input[type='checkbox']");

                if (del) {
                    del.checked = true;
                    row.style.display = "none";
                } else {
                    row.remove();
                    totalForms.value = tbody.querySelectorAll(`.${config.rowClass}`).length;
                }

                toggleTable();
            }
        });

        // =========================
        // PREVENT EMPTY ROWS
        // =========================
        document.querySelector("form").addEventListener("submit", function () {

            tbody.querySelectorAll(`.${config.rowClass}`).forEach(row => {

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
    }

    // =========================================
    // 🔥 INIT ALL FORMSETS HERE
    // =========================================

    setupDynamicFormset({
        selectName: "other_medical",
        tableId: "other-medical-table",
        addBtnId: "add-row",
        tbodyId: "other-body",
        totalFormsId: "id_othermedicals-TOTAL_FORMS",
        emptyFormId: "other-empty-form",
        rowClass: "other-row",
        removeBtnClass: "remove-row",
        yesValue: "1"
    });

    setupDynamicFormset({
        selectName: "nimregenin_herbal",
        tableId: "nimregenin-table",
        addBtnId: "add-nimregenin",
        tbodyId: "nimregenin-body",
        totalFormsId: "id_nimregenin-TOTAL_FORMS", // ✅ FIXED
        emptyFormId: "nimregenin-empty-form",
        rowClass: "nimregenin-row",
        removeBtnClass: "remove-nimregenin",
        yesValue: "1"
    });

    setupDynamicFormset({
        selectName: "other_herbal",
        tableId: "herbal-table",
        addBtnId: "add-herbal",
        tbodyId: "herbal-body",
        totalFormsId: "id_herbal-TOTAL_FORMS",
        emptyFormId: "herbal-empty-form",
        rowClass: "herbal-row",
        removeBtnClass: "remove-herbal",
        yesValue: "1"
    });

});