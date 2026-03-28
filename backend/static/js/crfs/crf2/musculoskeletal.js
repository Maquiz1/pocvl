document.addEventListener("DOMContentLoaded", function () {
    const musculoskeletalField = document.getElementById("id_musculoskeletal");
    const musculoskeletalComments = document.getElementById("musculoskeletal-comments");
    const musculoskeletalSignifcnt = document.getElementById("musculoskeletal-signifcnt");

    function togglemusculoskeletalFields() {
        if (musculoskeletalField.value === "2") {
            musculoskeletalComments.style.display = "table-cell";
            musculoskeletalSignifcnt.style.display = "table-cell";
        } else {
            musculoskeletalComments.style.display = "none";
            musculoskeletalSignifcnt.style.display = "none";
        }
    }

    // Run on load
    togglemusculoskeletalFields();

    // Run on change
    musculoskeletalField.addEventListener("change", togglemusculoskeletalFields);
});
