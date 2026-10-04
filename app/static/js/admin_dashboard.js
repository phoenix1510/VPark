document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('#facility-body tr[data-facility-id]');
    const checkboxes = document.querySelectorAll('.row-select');

    const viewBtn = document.getElementById('btn-view-floors');
    const viewRatesBtn = document.getElementById('btn-view-rates');
    const editBtn = document.getElementById('btn-edit-facility');
    const removeBtn = document.getElementById('btn-remove-facility');
    const addBtn = document.getElementById('btn-add-facility');

    const addBackdrop = document.getElementById('add-facility-backdrop');
    const cancelAddBtn = document.getElementById('btn-cancel-add');

    const editBackdrop = document.getElementById('edit-facility-backdrop');
    const cancelEditBtn = document.getElementById('btn-cancel-edit');
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');

    // Profile dropdown is independent of the facility-management controls below,
    // so wire it up (with null-checks) even if something else on the page is broken.
    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            profileDropdown.classList.toggle('open');
        });

        document.addEventListener('click', () => {
            profileDropdown.classList.remove('open');
        });
    }

    if (!viewBtn || !viewRatesBtn || !editBtn || !removeBtn || !addBtn || !addBackdrop || !cancelAddBtn || !editBackdrop || !cancelEditBtn) {
        console.error('VPark dashboard: one or more expected elements were not found on the page — check for duplicate IDs or a mismatched template.');
        return;
    }

    // Enforce single selection since actions operate on one facility_id at a time.
    function getSelectedId() {
        const checked = document.querySelector('.row-select:checked');
        if (!checked) return null;
        const val = (checked.value || '').trim();
        if (val && val !== 'on') return val;
        const row = checked.closest('tr');
        return row?.dataset?.facilityId || null;
    }

    function getSelectedRow() {
        const id = getSelectedId();
        if (!id) return null;
        return document.querySelector('#facility-body tr[data-facility-id="' + id + '"]');
    }

    function refreshActionState() {
        const id = getSelectedId();
        const hasSelection = !!id;

        viewBtn.classList.toggle('is-disabled', !hasSelection);
        viewRatesBtn.classList.toggle('is-disabled', !hasSelection);
        editBtn.classList.toggle('is-disabled', !hasSelection);
        removeBtn.classList.toggle('is-disabled', !hasSelection);

        rows.forEach(row => {
            row.classList.toggle('is-selected', row.dataset.facilityId === id);
        });
    }

    checkboxes.forEach(box => {
        box.addEventListener('change', function () {
            if (this.checked) {
                checkboxes.forEach(other => {
                    if (other !== this) other.checked = false;
                });
            }
            refreshActionState();
        });
    });

    // View Floors: plain anchor, JS supplies the facility_id and redirects to
    // /admin/<facility_id>/floors — no WTForm involved here.
    viewBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (viewBtn.classList.contains('is-disabled')) return;
        const id = getSelectedId();
        if (!id) return;
        window.location.href = '/admin/' + id + '/floors';
    });

    // View Rates: navigates to /admin/<facility_id>/rate.
    viewRatesBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (viewRatesBtn.classList.contains('is-disabled')) return;
        const id = getSelectedId();
        if (!id) return;
        window.location.href = '/admin/' + id + '/rate';
    });

    // Edit Facility: opens a modal backed by Edit_fal_Form, prefilled from the
    // selected row's current name/address so the admin edits in place.
    editBtn.addEventListener('click', function () {
        if (editBtn.classList.contains('is-disabled')) return;
        const id = getSelectedId();
        const row = getSelectedRow();
        if (!id || !row) return;

        const currentName = row.querySelector('.facility-name').textContent.trim();
        const currentAddress = row.children[2].textContent.trim();

        const editIdInput = document.getElementById('edit-facility-facility-id');
        if (editIdInput) editIdInput.value = id;
        document.getElementById('edit-facility-name').value = currentName;
        document.getElementById('edit-facility-address').value = currentAddress;

        editBackdrop.classList.add('open');
    });

    // Remove Facility: plain anchor, confirmed by typing "yes", then JS drops the
    // facility_id into the hidden form (backed by Remove_Fal_Form) and submits it.
    removeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (removeBtn.classList.contains('is-disabled')) return;
        const id = getSelectedId();
        if (!id) {
            alert('Please select a facility to remove.');
            return;
        }

        const typed = prompt('Type "yes" to confirm removing this facility:');
        if (!typed || typed.trim().toLowerCase() !== 'yes') return;

        const hiddenInput = document.getElementById('remove-facility-facility-id');
        const form = document.getElementById('remove-facility-form');
        if (!hiddenInput || !form) {
            console.error('Remove facility: hidden input or form not found.');
            return;
        }

        hiddenInput.value = id;
        form.submit();
    });

    addBtn.addEventListener('click', function () {
        addBackdrop.classList.add('open');
    });

    cancelAddBtn.addEventListener('click', function () {
        addBackdrop.classList.remove('open');
    });

    addBackdrop.addEventListener('click', function (e) {
        if (e.target === addBackdrop) addBackdrop.classList.remove('open');
    });

    cancelEditBtn.addEventListener('click', function () {
        editBackdrop.classList.remove('open');
    });

    editBackdrop.addEventListener('click', function (e) {
        if (e.target === editBackdrop) editBackdrop.classList.remove('open');
    });

    refreshActionState();
});