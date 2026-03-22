document.addEventListener("DOMContentLoaded", function () {

    function setupDynamicFormset(config) {

        const select = document.querySelector(`[name='${config.selectName}']`);
        const tableCard = document.getElementById(config.tableId);
        const addBtn = document.getElementById(config.addBtnId);
        const tbody = document.getElementById(config.tbodyId);
        const totalForms = document.getElementById(`id_${config.prefix}-TOTAL_FORMS`);
        const emptyForm = document.getElementById(config.emptyFormId);

        if (!select || !tableCard || !addBtn || !tbody || !totalForms || !emptyForm) {
            console.error("❌ Formset config error:", config);
            return;
        }

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

        addBtn.addEventListener("click", function () {

            let count = parseInt(totalForms.value);

            let template = emptyForm.innerHTML.replace(/__prefix__/g, count);

            const temp = document.createElement("tbody");
            temp.innerHTML = template;

            tbody.appendChild(temp.firstElementChild);

            totalForms.value = count + 1;

            toggleTable();
        });

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

    // ✅ CLEAN CALL

    setupDynamicFormset({
        prefix: "nimregenins",
        selectName: "nimregenin_herbal",
        tableId: "nimregenin-table",
        addBtnId: "add-nimregenin",
        tbodyId: "nimregenin-body",
        emptyFormId: "nimregenin-empty-form",
        rowClass: "nimregenin-row",
        removeBtnClass: "remove-nimregenin",
        yesValue: "1"
    });

});