document.addEventListener('DOMContentLoaded', function () {
    // ---- profile dropdown ----
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');
    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', (e) => { e.stopPropagation(); profileDropdown.classList.toggle('open'); });
        document.addEventListener('click', () => profileDropdown.classList.remove('open'));
    }

    // ---- Add Vehicle modal ----
    const addBackdrop  = document.getElementById('add-modal-backdrop');
    const openAddBtn   = document.getElementById('btn-open-add-modal');
    const closeAddBtn  = document.getElementById('btn-close-add-modal');

    function openAddModal()  { addBackdrop.classList.add('open'); }
    function closeAddModal() { addBackdrop.classList.remove('open'); }

    if (openAddBtn)  openAddBtn.addEventListener('click', openAddModal);
    if (closeAddBtn) closeAddBtn.addEventListener('click', closeAddModal);
    if (addBackdrop) addBackdrop.addEventListener('click', (e) => { if (e.target === addBackdrop) closeAddModal(); });

    // ---- Remove Vehicle modal ----
    const removeBackdrop   = document.getElementById('remove-modal-backdrop');
    const closeRemoveBtn   = document.getElementById('btn-close-remove-modal');
    const removeVehicleId  = document.getElementById('remove-vehicle-id');
    const removeVehicleName= document.getElementById('remove-vehicle-name');

    document.querySelectorAll('.btn-open-remove-modal').forEach((btn) => {
        btn.addEventListener('click', () => {
            const vid  = btn.dataset.vehicleId;
            const name = btn.dataset.vehicleName;
            removeVehicleId.value   = vid;
            removeVehicleName.textContent = name;
            removeBackdrop.classList.add('open');
            closeRemoveBtn.focus();
        });
    });

    if (closeRemoveBtn) closeRemoveBtn.addEventListener('click', () => removeBackdrop.classList.remove('open'));
    if (removeBackdrop) removeBackdrop.addEventListener('click', (e) => { if (e.target === removeBackdrop) removeBackdrop.classList.remove('open'); });

    // Escape closes whichever modal is open
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            addBackdrop && addBackdrop.classList.remove('open');
            removeBackdrop && removeBackdrop.classList.remove('open');
        }
    });
});
