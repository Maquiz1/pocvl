// $(document).ready(function () {

//     function handlePTTypeUI() {

//         const ptType = parseInt($("#id_pt_type").val());

//         // =========================
//         // DEFAULT: hide both sections
//         // =========================
//         $("#previous-section").hide();
//         $("#new-treatment-section").hide();

//         // =========================
//         // LOGIC
//         // =========================

//         if (ptType === 2) {
//             // 👉 ONLY previous treatment
//             $("#previous-section").show();

//         } else if (ptType === 3) {
//             // 👉 ONLY new treatment
//             $("#new-treatment-section").show();

//         } else if (ptType === 4) {
//             // 👉 BOTH (your new case 🔥)
//             $("#previous-section").show();
//             $("#new-treatment-section").show();
//         }
//     }

//     // =========================
//     // INIT
//     // =========================
//     handlePTTypeUI();

//     // =========================
//     // EVENTS
//     // =========================
//     $("#id_pt_type").change(function () {
//         handlePTTypeUI();
//     });

// });