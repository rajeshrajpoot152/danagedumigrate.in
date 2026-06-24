document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Dropdown toggles for mobile
    const mobileDropdowns = document.querySelectorAll('.mobile-dropdown-btn');
    mobileDropdowns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const dropdownContent = btn.nextElementSibling;
            if (dropdownContent) {
                dropdownContent.classList.toggle('hidden');
            }
        });
    });
});
