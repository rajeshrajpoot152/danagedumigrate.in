document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu Toggle
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
    
    // Counter Animation
    const counters = document.querySelectorAll('.animate-math .number');
    if (counters.length > 0) {
        const observer = new IntersectionObserver((entries, obs) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const counter = entry.target;
                    const target = +counter.getAttribute('data-to');
                    const duration = 2000; // 2 seconds
                    const increment = target / (duration / 16);

                    let current = 0;
                    const updateCounter = () => {
                        current += increment;
                        if (current < target) {
                            counter.innerText = Math.ceil(current);
                            requestAnimationFrame(updateCounter);
                        } else {
                            counter.innerText = target;
                        }
                    };
                    
                    updateCounter();
                    obs.unobserve(counter);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    }
    
    // Enquire Modal Logic
    const modal = document.getElementById('enquireModal');
    const modalInner = document.getElementById('enquireModalInner');
    const closeBtn = document.getElementById('closeEnquireModal');
    const triggerBtns = document.querySelectorAll('.popmake-551, .pum-trigger');
    
    if (modal && modalInner) {
        function openModal(e) {
            if (e) e.preventDefault();
            modal.classList.remove('opacity-0', 'pointer-events-none');
            modalInner.classList.remove('scale-95');
        }
        
        function closeModal() {
            modal.classList.add('opacity-0', 'pointer-events-none');
            modalInner.classList.add('scale-95');
        }
        
        triggerBtns.forEach(btn => {
            btn.addEventListener('click', openModal);
        });
        
        if (closeBtn) closeBtn.addEventListener('click', closeModal);
        
        // Close on clicking outside
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal();
        });
    }
});
