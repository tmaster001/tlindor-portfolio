document.addEventListener("DOMContentLoaded", function() {
    // Scrollspy for navbar active state
    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll(".nav-link");
    window.addEventListener("scroll", () => {
        let current = "";
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 120;
            if (pageYOffset >= sectionTop) {
                current = section.getAttribute("id");
            }
        });
        navLinks.forEach(link => {
            link.classList.remove("active");
            if (link.getAttribute("href") === "#" + current) {
                link.classList.add("active");
            }
        });
    });

    // Project filter logic
    const filterBtns = document.querySelectorAll('.filter-btn');
    const projectItems = document.querySelectorAll('.project-item');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            const tech = this.getAttribute('data-tech');
            projectItems.forEach(item => {
                if (tech === 'all' || item.getAttribute('data-tech').includes(tech)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
        // Dark mode toggle logic
        document.addEventListener('DOMContentLoaded', function () {
            const darkModeToggle = document.getElementById('dark-mode-toggle');
            if (darkModeToggle) {
                darkModeToggle.addEventListener('click', () => {
                    document.body.classList.toggle('dark-mode');
                });
            }
        });
    }); // <-- closes filterBtns.forEach callback

}); // <-- closes main DOMContentLoaded event listener
