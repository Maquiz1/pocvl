document.addEventListener("DOMContentLoaded", function () {

    const trigger = document.getElementById("id_physical_exams_other");
    const tableCard = document.getElementById("other-exams-section");
    const addBtn = document.getElementById("add-other-exam");
    const tbody = document.getElementById("other-exams-body");
    const totalForms = document.querySelector("input[name='otherexams-TOTAL_FORMS']");
    const emptyForm = document.getElementById("other-exams-empty-form");

    // console.log({
    //     trigger,
    //     tableCard,
    //     addBtn,
    //     tbody,
    //     totalForms,
    //     emptyForm
    // });

    // 🔥 SAFETY CHECK
    if (!trigger || !tableCard || !addBtn || !tbody || !totalForms || !emptyForm) {
        console.error("❌ Other Physical Exams setup failed");
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
        const hasRows = tbody.querySelectorAll(
            ".other-exams-row:not([style*='display: none'])"
        ).length > 0;

        if (isYes(trigger) || hasRows) {
            tableCard.style.display = "block";
        } else {
            tableCard.style.display = "none";
        }

        addBtn.disabled = !isYes(trigger);
    }

    trigger.addEventListener("change", toggleTable);
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
        if (e.target.classList.contains("remove-other-exam")) {
            const row = e.target.closest("tr");
            const del = row.querySelector("input[type='checkbox']");

            if (del) {
                del.checked = true;
                row.style.display = "none";
            } else {
                row.remove();
                totalForms.value = tbody.querySelectorAll(".other-exams-row").length;
            }

            toggleTable();
        }
    });

});
