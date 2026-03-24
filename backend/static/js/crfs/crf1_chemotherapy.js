document.addEventListener("DOMContentLoaded", function () {

    const ChemotherapyPerformed = document.getElementById("id_chemotherapy_performed");
    const tableCard = document.getElementById("chemo-table");
    const addBtn = document.getElementById("add-chemo");
    const tbody = document.getElementById("chemo-body");
    const totalForms = document.getElementById("id_chemotherapies-TOTAL_FORMS");

    function toggleTable() {
        const valText = ChemotherapyPerformed.options[ChemotherapyPerformed.selectedIndex].text.toLowerCase();

        const hasRows = tbody.querySelectorAll(".chemo-row:not([style*='display: none'])").length > 0;

        if (valText === "yes" || hasRows) {
            tableCard.style.display = "";
        } else {
            tableCard.style.display = "none";
        }

        // ✅ HERE
        addBtn.disabled = valText !== "yes";
    }

    ChemotherapyPerformed.addEventListener("change", toggleTable);
    toggleTable();

    addBtn.addEventListener("click", function () {
        let count = parseInt(totalForms.value);
        let template = document.getElementById("chemo-empty").innerHTML.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        tbody.appendChild(temp.firstElementChild);
        totalForms.value = count + 1;

        toggleTable();
    });

    tbody.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-chemo")) {
            const row = e.target.closest("tr");
            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                del.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                totalForms.value = tbody.querySelectorAll(".chemo-row").length;
            }

            toggleTable();
        }
    });

    tbody.addEventListener("change", function (e) {
        if (e.target.name.includes("chemotherapy_ongoing")) {
            const row = e.target.closest("tr");
            const end = row.querySelector("input[name*='chemotherapy_end']");

            if (e.target.value === "1") {
                end.value = "";
                end.closest("td").style.display = "none";
            } else {
                end.closest("td").style.display = "";
            }
        }
    });

});