document.addEventListener("DOMContentLoaded", function () {

    const NimregeninHerbal = document.getElementById("id_nimregenin_herbal");
    const tableCard = document.getElementById("nimregenin-table");
    const addBtn = document.getElementById("add-nimregenin");
    const tbody = document.getElementById("nimregenin-body");
    const totalForms = document.getElementById("id_nimregenins-TOTAL_FORMS");
    const emptyForm = document.getElementById("nimregenin-empty-form");

    // 🔥 SAFETY CHECK
    if (!NimregeninHerbal || !tableCard || !addBtn || !tbody || !totalForms || !emptyForm) {
        console.error("❌ Nimregenin setup failed");
        return;
    }else {
        console.error("Good Nimregeini");

    }

    function isYes(select) {
        return ["1", "yes", "true", "True"].includes(select.value);
    }

    function toggleTable() {
        const hasRows = tbody.querySelectorAll(
            ".nimregenin-row:not([style*='display: none'])"
        ).length > 0;

        if (isYes(NimregeninHerbal) || hasRows) {
            tableCard.style.display = "block";
        } else {
            tableCard.style.display = "none";
        }

        addBtn.disabled = !isYes(NimregeninHerbal);
    }

    NimregeninHerbal.addEventListener("change", toggleTable);
    toggleTable();

    // =========================
    // ADD ROW
    // =========================
    addBtn.addEventListener("click", function () {

        let count = parseInt(totalForms.value) || 0;

        let template = emptyForm.innerHTML.replace(/__prefix__/g, count);

        const temp = document.createElement("tbody");
        temp.innerHTML = template;

        const newRow = temp.firstElementChild;
        if (!newRow) return;

        tbody.appendChild(newRow);

        totalForms.value = count + 1;

        toggleTable();
    });

    // =========================
    // REMOVE ROW
    // =========================
    tbody.addEventListener("click", function (e) {

        if (e.target.classList.contains("remove-nimregenin")) {

            const row = e.target.closest("tr");
            if (!row) return;

            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                del.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                totalForms.value = tbody.querySelectorAll(".nimregenin-row").length;
            }

            toggleTable();
        }
    });

});