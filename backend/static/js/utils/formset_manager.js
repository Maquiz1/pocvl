document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll("[data-formset]").forEach(container => {

        const prefix = container.dataset.prefix;

        const table = container.querySelector("[data-table]");
        const tbody = container.querySelector("[data-body]");
        const addBtn = container.querySelector("[data-add]");
        const emptyForm = container.querySelector("[data-empty-form]");
        const totalForms = document.querySelector(
            `input[name='${prefix}-TOTAL_FORMS']`
        );

        if (!table || !tbody || !addBtn || !emptyForm || !totalForms) {
            console.error(`❌ Formset ${prefix} not initialized`);
            return;
        }

        // =========================
        // ADD ROW
        // =========================
        addBtn.addEventListener("click", function () {

            let formCount = parseInt(totalForms.value);

            let template = emptyForm.innerHTML.trim();

            template = template.replaceAll("__prefix__", formCount);

            const temp = document.createElement("tbody");
            temp.innerHTML = template;

            const newRow = temp.firstElementChild;

            tbody.appendChild(newRow);

            totalForms.value = formCount + 1;
        });

        // =========================
        // REMOVE ROW
        // =========================
        tbody.addEventListener("click", function (e) {

            if (e.target.classList.contains("remove-row")) {

                const row = e.target.closest("tr");

                const delInput = row.querySelector("input[name$='-DELETE']");

                if (delInput) {
                    delInput.checked = true;
                    row.style.display = "none";
                } else {
                    row.remove();
                }
            }
        });

    });

});