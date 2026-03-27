document.addEventListener("DOMContentLoaded", function () {

    const SurgeryPerformed = document.getElementById("id_surgery_performed");
    const tableCard = document.getElementById("surgery-table");
    const addBtn = document.getElementById("add-surgery");
    const tbody = document.getElementById("surgery-body");
    const totalForms = document.getElementById("id_surgeries-TOTAL_FORMS");

    function toggleTable() {
        const valText = SurgeryPerformed.options[SurgeryPerformed.selectedIndex].text.toLowerCase();

        const hasRows = tbody.querySelectorAll(".surgery-row:not([style*='display: none'])").length > 0;

        if (valText === "yes" || hasRows) {
            tableCard.style.display = "";
        } else {
            tableCard.style.display = "none";
        }

        // ✅ HERE
        addBtn.disabled = valText !== "yes";
    }

    SurgeryPerformed.addEventListener("change", toggleTable);
    toggleTable();

    addBtn.addEventListener("click", function () {
        let count = parseInt(totalForms.value);
        let template = document.getElementById("surgery-empty").innerHTML.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        tbody.appendChild(temp.firstElementChild);
        totalForms.value = count + 1;

        toggleTable();
    });

    tbody.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-surgery")) {
            const row = e.target.closest("tr");
            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                del.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                totalForms.value = tbody.querySelectorAll(".surgery-row").length;
            }

            toggleTable();
        }
    });

});