document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('#floor-body tr[data-floor-id]');
    const checkboxes = document.querySelectorAll('.row-select');

    const viewBtn = document.getElementById('btn-view-slots');
    const addBtn = document.getElementById('btn-add-floor');
    const removeBtn = document.getElementById('btn-remove-floor');

    const addBackdrop = document.getElementById('add-floor-backdrop');
    const cancelAddBtn = document.getElementById('btn-cancel-add-floor');

    if (!viewBtn || !addBtn || !removeBtn || !addBackdrop || !cancelAddBtn) {
        console.error('VPark floors: one or more expected elements were not found on the page — check for duplicate IDs or a mismatched template.');
        return;
    }

    // Enforce single selection since actions operate on one floor_id at a time.
    function getSelectedId() {
        const checked = document.querySelector('.row-select:checked');
        return checked ? checked.value : null;
    }

    function refreshActionState() {
        const id = getSelectedId();
        const hasSelection = !!id;

        viewBtn.classList.toggle('is-disabled', !hasSelection);
        removeBtn.classList.toggle('is-disabled', !hasSelection);

        rows.forEach(row => {
            row.classList.toggle('is-selected', row.dataset.floorId === id);
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

    // View Slots: plain anchor, JS supplies the floor_id and redirects to
    // <current facility floors path>/<floor_id>/slots — no WTForm involved here.
    const facilityId = document.querySelector('main').dataset.facilityId;

    viewBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (viewBtn.classList.contains('is-disabled')) return;
        const id = getSelectedId();
        if (!id) return;
        window.location.href = `/admin/${facilityId}/${id}/Slots`;
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

    // Remove Floor: plain anchor, confirmed by typing "yes", then JS drops the
    // floor_id into the hidden form (backed by Remove_Floor_Form) and submits it.
    removeBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (removeBtn.classList.contains('is-disabled')) return;
        const id = getSelectedId();
        if (!id) return;

        const typed = prompt('Type "yes" to confirm removing this floor:');
        if (!typed || typed.trim().toLowerCase() !== 'yes') return;

        document.getElementById('remove-floor-floor-id').value = id;
        document.getElementById('remove-floor-form').submit();
    });

    refreshActionState();
});