document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('searchInput');
    const rows = document.querySelectorAll('.user-table tbody tr');

    if (searchInput) {
        searchInput.addEventListener('input', function () {
            const keyword = searchInput.value.trim().toLowerCase();

            rows.forEach(function (row) {
                const name = row.dataset.name || '';
                const email = row.dataset.email || '';
                const match = !keyword || name.includes(keyword) || email.includes(keyword);
                row.style.display = match ? '' : 'none';
            });
        });
    }

    const deleteLinks = document.querySelectorAll('.delete-btn');

    deleteLinks.forEach(function (link) {
        link.addEventListener('click', function (event) {
            const name = link.dataset.name || 'người dùng này';
            const confirmDelete = window.confirm('Bạn có chắc muốn xóa ' + name + '?');
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    });

    const forms = document.querySelectorAll('.user-form, .inline-form');
    forms.forEach(function (form) {
        form.addEventListener('submit', function () {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.textContent = 'Đang lưu...';
            }
        });
    });
});
