document.addEventListener("DOMContentLoaded", function () {
    const rowCheckboxes = () => Array.from(document.querySelectorAll("#rate-body .row-select"));

    const btnAddRate     = document.getElementById("btn-add-rate");
    const btnRemoveRate  = document.getElementById("btn-remove-rate");

    const addRateBackdrop   = document.getElementById("add-rate-backdrop");
    const btnCancelAddRate  = document.getElementById("btn-cancel-add-rate");

    const removeRateForm    = document.getElementById("remove-rate-form");
    const removeRateIdInput = document.getElementById("remove-rate-rate-id");

    function getSelectedRow() {
        const checked = rowCheckboxes().filter(cb => cb.checked);
        if (checked.length !== 1) return null;
        return checked[0].closest("tr");
    }

    function updateActionState() {
        const exactlyOne = rowCheckboxes().filter(cb => cb.checked).length === 1;
        if (btnRemoveRate) btnRemoveRate.classList.toggle("is-disabled", !exactlyOne);
    }

    // Single-select enforcement
    rowCheckboxes().forEach(cb => {
        cb.addEventListener("change", function () {
            if (this.checked) {
                rowCheckboxes().forEach(other => {
                    if (other !== this) other.checked = false;
                });
            }
            updateActionState();
        });
    });

    // --- Add Rate modal ---
    if (btnAddRate && addRateBackdrop) {
        btnAddRate.addEventListener("click", function () {
            addRateBackdrop.classList.add("open");
        });
    }
    if (btnCancelAddRate && addRateBackdrop) {
        btnCancelAddRate.addEventListener("click", function () {
            addRateBackdrop.classList.remove("open");
        });
    }
    if (addRateBackdrop) {
        addRateBackdrop.addEventListener("click", function (e) {
            if (e.target === addRateBackdrop) addRateBackdrop.classList.remove("open");
        });
    }

    // --- Remove Rate ---
    if (btnRemoveRate) {
        btnRemoveRate.addEventListener("click", function (e) {
            e.preventDefault();
            if (btnRemoveRate.classList.contains("is-disabled")) return;

            const row = getSelectedRow();
            if (!row) return;

            const rateId = row.getAttribute("data-rate-id");
            const labelEl = row.querySelector(".facility-name");
            const label = labelEl ? labelEl.textContent.trim() : "this rate";

            if (!confirm(`Remove rate for "${label}"? This cannot be undone.`)) return;

            removeRateIdInput.value = rateId;
            removeRateForm.submit();
        });
    }

    updateActionState();
});
