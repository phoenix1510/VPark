document.addEventListener('DOMContentLoaded', function () {
    // ---- profile dropdown ----
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');
    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', (e) => { e.stopPropagation(); profileDropdown.classList.toggle('open'); });
        document.addEventListener('click', () => profileDropdown.classList.remove('open'));
    }

    // ---- data & state ----
    const userVehiclesEl = document.getElementById('user-vehicles-data');
    let USER_VEHICLES = [];
    if (userVehiclesEl && userVehiclesEl.textContent.trim()) {
        try {
            USER_VEHICLES = JSON.parse(userVehiclesEl.textContent);
        } catch (err) {
            console.error('Failed to parse USER_VEHICLES JSON:', err);
        }
    }

    let currentFacilityId = null;
    let selectedSlotId    = null;
    let selectedVehicleId = null;

    const backdrop     = document.getElementById('slots-modal-backdrop');
    const stepSlots    = document.getElementById('step-slots');
    const stepVehicle  = document.getElementById('step-vehicle');
    const slotsGrid    = document.getElementById('slots-grid');
    const ratesList    = document.getElementById('rates-list');
    const loadingMsg   = document.getElementById('slots-loading');
    const modalTitle   = document.getElementById('slots-modal-title');
    const selectedSlotDisplay = document.getElementById('selected-slot-display');
    const vehicleListEl = document.getElementById('vehicle-list-modal');

    const formSlotId     = document.getElementById('form-slot-id');
    const formFacilityId = document.getElementById('form-facility-id');
    const formVehicleId  = document.getElementById('form-vehicle-id');
    const confirmBtn     = document.getElementById('btn-confirm-park');

    function openModal() { backdrop.classList.add('open'); }
    function closeModal() {
        backdrop.classList.remove('open');
        resetModal();
    }
    function resetModal() {
        currentFacilityId = null;
        selectedSlotId    = null;
        selectedVehicleId = null;
        slotsGrid.innerHTML = '';
        ratesList.innerHTML = '';
        showStep('slots');
        if (confirmBtn) confirmBtn.disabled = true;
    }
    function showStep(step) {
        if (step === 'slots') {
            stepSlots.classList.remove('hidden');
            stepVehicle.classList.add('hidden');
        } else {
            stepSlots.classList.add('hidden');
            stepVehicle.classList.remove('hidden');
        }
    }

    // ---- Open modal on "View Slots" click ----
    document.querySelectorAll('.btn-view-slots').forEach((btn) => {
        btn.addEventListener('click', async () => {
            currentFacilityId = btn.dataset.facilityId;
            modalTitle.textContent = btn.dataset.facilityName || 'Slots';
            showStep('slots');
            openModal();

            // fetch slots + rates
            slotsGrid.innerHTML = '';
            ratesList.innerHTML = '';
            loadingMsg.classList.add('visible');

            try {
                const res  = await fetch(`/user/dashboard/search_facility/${currentFacilityId}`);
                const data = await res.json();
                loadingMsg.classList.remove('visible');
                renderSlots(data.slots || []);
                renderRates(data.parking_rates || []);
            } catch (err) {
                loadingMsg.textContent = 'Failed to load slots. Please try again.';
                console.error(err);
            }
        });
    });

    function renderSlots(slots) {
        if (!slots.length) {
            slotsGrid.innerHTML = '<p style="color:var(--concrete-dim);font-size:0.88rem">No slots available at this facility.</p>';
            return;
        }
        slots.forEach((slot) => {
            const btn = document.createElement('button');
            btn.type = 'button';
            const isVacant = slot.status === 'vacant';
            btn.className = `slot-btn ${isVacant ? 'vacant' : 'occupied'}`;
            btn.disabled = !isVacant;
            btn.innerHTML = `<span class="slot-num">${slot.slot_number}</span><span class="slot-status">${slot.status}</span>`;
            btn.dataset.slotId = slot.slot_id;

            if (isVacant) {
                btn.addEventListener('click', () => selectSlot(btn, slot));
            }
            slotsGrid.appendChild(btn);
        });
    }

    function selectSlot(btn, slot) {
        // deselect previous
        slotsGrid.querySelectorAll('.slot-btn.selected').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        selectedSlotId = slot.slot_id;
        selectedSlotDisplay.textContent = slot.slot_number;

        // populate vehicle step
        renderVehicleList();
        showStep('vehicle');
    }

    function renderRates(rates) {
        if (!rates.length) {
            ratesList.innerHTML = '<span style="font-size:0.82rem;color:var(--concrete-dim)">No rates configured.</span>';
            return;
        }
        rates.forEach((r) => {
            const chip = document.createElement('span');
            chip.className = 'rate-chip';
            chip.textContent = `${r.vehicle_type} — ₹${r.rate_per_hour}/hr`;
            ratesList.appendChild(chip);
        });
    }

    function renderVehicleList() {
        vehicleListEl.innerHTML = '';
        selectedVehicleId = null;
        if (confirmBtn) confirmBtn.disabled = true;

        if (!USER_VEHICLES || !USER_VEHICLES.length) {
            vehicleListEl.innerHTML = '<p style="font-size:0.88rem;color:var(--concrete-dim)">No vehicles added. <a href="/user/dashboard/vehicles" style="color:var(--yellow)">Add one first.</a></p>';
            return;
        }

        USER_VEHICLES.forEach((v) => {
            const label = document.createElement('label');
            label.className = 'vehicle-option';

            const radio = document.createElement('input');
            radio.type = 'radio';
            radio.name = 'vehicle_select';
            radio.value = v.vehicle_id;

            radio.addEventListener('change', () => {
                document.querySelectorAll('.vehicle-option').forEach(el => el.classList.remove('selected'));
                label.classList.add('selected');
                selectedVehicleId = v.vehicle_id;
                // populate hidden form fields
                formSlotId.value     = selectedSlotId;
                formFacilityId.value = currentFacilityId;
                formVehicleId.value  = selectedVehicleId;
                if (confirmBtn) confirmBtn.disabled = false;
            });

            const info = document.createElement('div');
            info.className = 'vehicle-option-info';
            info.innerHTML = `<div class="vehicle-option-name">${v.vehicle_name}</div><div class="vehicle-option-reg">${v.registration_number} &middot; ${v.vehicle_type}</div>`;

            label.appendChild(radio);
            label.appendChild(info);
            vehicleListEl.appendChild(label);
        });
    }

    // ---- Close buttons ----
    document.getElementById('btn-close-slots-modal')?.addEventListener('click', closeModal);
    document.getElementById('btn-close-slots-modal-2')?.addEventListener('click', closeModal);
    document.getElementById('btn-back-to-slots')?.addEventListener('click', () => {
        selectedSlotId = null;
        slotsGrid.querySelectorAll('.slot-btn.selected').forEach(b => b.classList.remove('selected'));
        if (confirmBtn) confirmBtn.disabled = true;
        showStep('slots');
    });

    // Click outside modal box
    backdrop?.addEventListener('click', (e) => { if (e.target === backdrop) closeModal(); });

    // Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && backdrop.classList.contains('open')) closeModal();
    });
});
