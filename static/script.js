document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const cards = document.querySelectorAll('.product-card');

    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const keyword = searchInput.value.trim().toLowerCase();

            cards.forEach(function (card) {
                const name = (card.dataset.name || '').toLowerCase();
                const price = (card.dataset.price || '').toLowerCase();
                const match = !keyword || name.includes(keyword) || price.includes(keyword);
                card.style.display = match ? 'flex' : 'none';
            });
        });
    }

    const forms = document.querySelectorAll('.user-form');
    forms.forEach(function (form) {
        form.addEventListener('submit', function () {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Đang thêm...';
            }
        });
    });
});
