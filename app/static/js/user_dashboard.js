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

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && profileDropdown.classList.contains('open')) {
                profileDropdown.classList.remove('open');
            }
        });
    }

    // Quick search bar autofocus helper when typing '/' outside inputs
    const searchInput = document.querySelector('.quick-search-bar .search-input');
    if (searchInput) {
        document.addEventListener('keydown', (e) => {
            if (e.key === '/' && document.activeElement !== searchInput && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
                e.preventDefault();
                searchInput.focus();
            }
        });
    }
});
