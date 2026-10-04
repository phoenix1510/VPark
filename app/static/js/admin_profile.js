document.addEventListener('DOMContentLoaded', function () {
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');

    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            profileDropdown.classList.toggle('open');
        });

        document.addEventListener('click', () => {
            profileDropdown.classList.remove('open');
        });
    }

    const editBtn = document.getElementById('btn-edit-profile');
    const cancelBtn = document.getElementById('btn-cancel-edit-profile');
    const viewBlock = document.getElementById('profile-view');
    const editForm = document.getElementById('profile-edit-form');

    if (!editBtn || !cancelBtn || !viewBlock || !editForm) {
        console.error('VPark profile: one or more expected elements were not found on the page.');
        return;
    }

    function enterEditMode() {
        viewBlock.style.display = 'none';
        editBtn.style.display = 'none';
        editForm.classList.add('open');
    }

    function exitEditMode() {
        // Reset any unsaved edits back to the values rendered by the server.
        editForm.reset();
        editForm.classList.remove('open');
        viewBlock.style.display = '';
        editBtn.style.display = '';
    }

    editBtn.addEventListener('click', enterEditMode);
    cancelBtn.addEventListener('click', exitEditMode);

    const openDeleteBtn = document.getElementById('btn-open-delete-modal');
    const closeDeleteBtn = document.getElementById('btn-close-delete-modal');
    const deleteOverlay = document.getElementById('delete-modal-overlay');

    if (openDeleteBtn && closeDeleteBtn && deleteOverlay) {
        function openDeleteModal() {
            deleteOverlay.classList.add('open');
            closeDeleteBtn.focus();
        }

        function closeDeleteModal() {
            deleteOverlay.classList.remove('open');
            openDeleteBtn.focus();
        }

        openDeleteBtn.addEventListener('click', openDeleteModal);
        closeDeleteBtn.addEventListener('click', closeDeleteModal);

        // Close on backdrop click
        deleteOverlay.addEventListener('click', (e) => {
            if (e.target === deleteOverlay) closeDeleteModal();
        });

        // Close on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && deleteOverlay.classList.contains('open')) {
                closeDeleteModal();
            }
        });
    }
});
