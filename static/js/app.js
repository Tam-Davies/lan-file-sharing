document.addEventListener("DOMContentLoaded", () => {

    /* ================================
       THEME TOGGLE
    ================================= */

    const themeToggle = document.getElementById("themeToggle");

    const savedTheme = localStorage.getItem("tammydx-theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark");

        if (themeToggle) {
            themeToggle.textContent = "☀";
        }
    }

    if (themeToggle) {
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
    }


    /* ================================
       FILE SELECTION
    ================================= */

    const fileInput = document.getElementById("file");
    const fileLabel = document.querySelector(".file-input span");

    if (fileInput && fileLabel) {

        fileInput.addEventListener("change", () => {

            if (fileInput.files.length > 0) {

                const selectedFile = fileInput.files[0];

                fileLabel.textContent =
                    selectedFile.name;

            } else {

                fileLabel.textContent =
                    "Choose File";
            }

        });
    }


    /* ================================
       HIGHLIGHT NAVIGATION ITEM
    ================================= */

    const sections =
        document.querySelectorAll(".section");

    const navLinks =
        document.querySelectorAll(".nav-link");

    if (sections.length && navLinks.length) {

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
    }

});