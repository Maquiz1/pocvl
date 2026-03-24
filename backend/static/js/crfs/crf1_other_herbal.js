document.addEventListener("DOMContentLoaded", function () {

    const OtherHerbal = document.getElementById("id_other_herbal");
    const tableCard = document.getElementById("herbal-table");
    const addBtn = document.getElementById("add-herbal");
    const tbody = document.getElementById("herbal-body");
    const totalForms = document.getElementById("id_herbal-TOTAL_FORMS");

    function toggleTable() {
        const valText = OtherHerbal.options[OtherHerbal.selectedIndex].text.toLowerCase();

        const hasRows = tbody.querySelectorAll(".herbal-row:not([style*='display: none'])").length > 0;

        if (valText === "yes" || hasRows) {
            tableCard.style.display = "";
        } else {
            tableCard.style.display = "none";
        }

        // ✅ HERE
        addBtn.disabled = valText !== "yes";
    }

    OtherHerbal.addEventListener("change", toggleTable);
    toggleTable();

    addBtn.addEventListener("click", function () {
        let count = parseInt(totalForms.value);
        let template = document.getElementById("herbal-empty-form").innerHTML.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        tbody.appendChild(temp.firstElementChild);
        totalForms.value = count + 1;

        toggleTable();
    });

    tbody.addEventListener("click", function (e) {
        if (e.target.classList.contains("remove-herbal")) {
            const row = e.target.closest("tr");
            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                del.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                totalForms.value = tbody.querySelectorAll(".herbal-row").length;
            }

            toggleTable();
        }
    });

});