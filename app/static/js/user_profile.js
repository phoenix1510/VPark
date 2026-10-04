document.addEventListener('DOMContentLoaded', function () {
    // ---- Profile dropdown menu toggle ----
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

    // ---- Delete Account Modal ----
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
