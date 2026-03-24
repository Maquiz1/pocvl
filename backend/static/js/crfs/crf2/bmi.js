function calculateBMI() {
    let h = parseFloat(id_height.value);
    let w = parseFloat(id_weight.value);
    if (h && w) id_bmi.value = (w / ((h / 100) ** 2)).toFixed(2);
}

id_height?.addEventListener("input", calculateBMI);
id_weight?.addEventListener("input", calculateBMI);

/* highlight invalid */
document.querySelectorAll(".field-error").forEach(e => {
    if (e.innerText.trim() !== "") {
        e.previousElementSibling?.classList.add("is-invalid");
    }
});
