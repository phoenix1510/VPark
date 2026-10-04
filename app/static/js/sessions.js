document.addEventListener('DOMContentLoaded', function () {
    // ---- profile dropdown ----
    const profileBtn = document.getElementById('profile-btn');
    const profileDropdown = document.getElementById('profile-dropdown');
    if (profileBtn && profileDropdown) {
        profileBtn.addEventListener('click', (e) => { e.stopPropagation(); profileDropdown.classList.toggle('open'); });
        document.addEventListener('click', () => profileDropdown.classList.remove('open'));
    }

    // ---- Finish session modal ----
    const finishBackdrop     = document.getElementById('finish-modal-backdrop');
    const closeFinishBtn     = document.getElementById('btn-close-finish-modal');
    const finishSessionId    = document.getElementById('finish-session-id');
    const finishSessionDisp  = document.getElementById('finish-session-id-display');
    const finishForm         = document.getElementById('finish-session-form');

    document.querySelectorAll('.btn-open-finish-modal').forEach((btn) => {
        btn.addEventListener('click', () => {
            const sid = btn.dataset.sessionId;
            finishSessionId.value         = sid;
            finishSessionDisp.textContent = sid;
            finishBackdrop.classList.add('open');
            closeFinishBtn.focus();
        });
    });

    if (closeFinishBtn) closeFinishBtn.addEventListener('click', () => finishBackdrop.classList.remove('open'));
    finishBackdrop?.addEventListener('click', (e) => { if (e.target === finishBackdrop) finishBackdrop.classList.remove('open'); });

    // ---- Summary modal ----
    const summaryBackdrop = document.getElementById('summary-modal-backdrop');
    const sumDuration     = document.getElementById('sum-duration');
    const sumHours        = document.getElementById('sum-hours');
    const sumAmount       = document.getElementById('sum-amount');
    const closeSummaryBtn = document.getElementById('btn-close-summary');

    function showSummary(data) {
        sumDuration.textContent = data.duration;
        sumHours.textContent    = data.duration_hours + ' hr';
        sumAmount.textContent   = '₹' + data.final_amount;
        finishBackdrop.classList.remove('open');
        summaryBackdrop.classList.add('open');
    }

    closeSummaryBtn?.addEventListener('click', () => {
        summaryBackdrop.classList.remove('open');
        // Reload to refresh session list
        window.location.reload();
    });

    // ---- Intercept finish form for AJAX ----
    // Finish_parking returns JSON on success; fall back to normal redirect otherwise.
    if (finishForm) {
        finishForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(finishForm);
            try {
                const res = await fetch(finishForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                if (res.ok) {
                    const contentType = res.headers.get('content-type') || '';
                    if (contentType.includes('application/json')) {
                        const data = await res.json();
                        showSummary(data);
                    } else {
                        // Server redirected (e.g. already ended session)
                        window.location.href = res.url;
                    }
                } else {
                    window.location.reload();
                }
            } catch (err) {
                console.error('Finish session error:', err);
                finishForm.submit(); // fallback
            }
        });
    }

    // ---- Escape key ----
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            finishBackdrop?.classList.remove('open');
            summaryBackdrop?.classList.remove('open');
        }
    });
});
