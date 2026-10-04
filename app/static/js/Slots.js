document.addEventListener('DOMContentLoaded', function () {
    const rowCheckboxes = () => Array.from(document.querySelectorAll('#slot-body .row-select'));

    const btnEditStatus = document.getElementById('btn-edit-status');
    const btnRemoveSlot = document.getElementById('btn-remove-slot');

    const removeForm = document.getElementById('remove-slot-form');
    const removeSlotIdInput = document.getElementById('remove-slot-slot-id');

    const editStatusBackdrop = document.getElementById('edit-status-backdrop');
    const editStatusSlotIdInput = document.getElementById('edit-status-slot-id');
    const editStatusSelect = document.getElementById('edit-status-value');

    const addSlotBackdrop = document.getElementById('add-slot-backdrop');
    const btnAddSlot = document.getElementById('btn-add-slot');
    const btnCancelAddSlot = document.getElementById('btn-cancel-add-slot');
    const btnCancelEditStatus = document.getElementById('btn-cancel-edit-status');

    function getSelectedRow() {
        const checked = rowCheckboxes().filter(cb => cb.checked);
        if (checked.length !== 1) return null;
        return checked[0].closest('tr');
    }

    function updateActionState() {
        const checked = rowCheckboxes().filter(cb => cb.checked);
        const exactlyOne = checked.length === 1;

        [btnEditStatus, btnRemoveSlot].forEach(btn => {
            if (!btn) return;
            btn.classList.toggle('is-disabled', !exactlyOne);
        });
    }

    // Only allow one row selected at a time, mirroring floors.html's single-select behavior
    rowCheckboxes().forEach(cb => {
        cb.addEventListener('change', function () {
            if (this.checked) {
                rowCheckboxes().forEach(other => {
                    if (other !== this) other.checked = false;
                });
            }
            updateActionState();
        });
    });

    // --- Add Slot modal ---
    if (btnAddSlot && addSlotBackdrop) {
        btnAddSlot.addEventListener('click', function () {
            addSlotBackdrop.classList.add('open');
        });
    }
    if (btnCancelAddSlot && addSlotBackdrop) {
        btnCancelAddSlot.addEventListener('click', function () {
            addSlotBackdrop.classList.remove('open');
        });
    }

    // --- Edit Status modal ---
    if (btnEditStatus) {
        btnEditStatus.addEventListener('click', function (e) {
            e.preventDefault();
            if (btnEditStatus.classList.contains('is-disabled')) return;

            const row = getSelectedRow();
            if (!row) return;

            const slotId = row.getAttribute('data-slot-id');
            const currentStatus = row.getAttribute('data-status');

            editStatusSlotIdInput.value = slotId;
            if (currentStatus) {
                editStatusSelect.value = currentStatus;
            }

            editStatusBackdrop.classList.add('open');
        });
    }
    if (btnCancelEditStatus && editStatusBackdrop) {
        btnCancelEditStatus.addEventListener('click', function () {
            editStatusBackdrop.classList.remove('open');
        });
    }

    // --- Remove Slot ---
    if (btnRemoveSlot) {
        btnRemoveSlot.addEventListener('click', function (e) {
            e.preventDefault();
            if (btnRemoveSlot.classList.contains('is-disabled')) return;

            const row = getSelectedRow();
            if (!row) return;

            const slotId = row.getAttribute('data-slot-id');
            const slotNumberEl = row.querySelector('.facility-name');
            const label = slotNumberEl ? slotNumberEl.textContent : 'this slot';

            if (!confirm(`Remove ${label}? This cannot be undone.`)) return;

            removeSlotIdInput.value = slotId;
            removeForm.submit();
        });
    }

    // Close modals on backdrop click (outside the modal card)
    [addSlotBackdrop, editStatusBackdrop].forEach(backdrop => {
        if (!backdrop) return;
        backdrop.addEventListener('click', function (e) {
            if (e.target === backdrop) {
                backdrop.classList.remove('open');
            }
        });
    });

    updateActionState();
});