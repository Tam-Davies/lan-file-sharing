document.addEventListener("DOMContentLoaded", () => {

    const themeToggle = document.getElementById("themeToggle");

    const savedTheme = localStorage.getItem("tammydx-theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark");
        themeToggle.textContent = "☀";
    }

    themeToggle.addEventListener("click", () => {

        document.body.classList.toggle("dark");

        const darkMode =
            document.body.classList.contains("dark");

        localStorage.setItem(
            "tammydx-theme",
            darkMode ? "dark" : "light"
        );

        themeToggle.textContent =
            darkMode ? "☀" : "☾";
    });


    /* Highlight navigation item */

    const sections =
        document.querySelectorAll(".section");

    const navLinks =
        document.querySelectorAll(".nav-link");

    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(entry => {

                    if (!entry.isIntersecting) {
                        return;
                    }

                    navLinks.forEach(link => {
                        link.classList.remove("active");
                    });

                    const active =
                        document.querySelector(
                            `.nav-link[href="#${entry.target.id}"]`
                        );

                    if (active) {
                        active.classList.add("active");
                    }

                });

            },
            {
                threshold: 0.25
            }
        );

    sections.forEach(section => {
        observer.observe(section);
    });

});