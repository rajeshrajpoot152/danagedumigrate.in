document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        
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
});

