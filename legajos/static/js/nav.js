  document.addEventListener("DOMContentLoaded", function () {
    const navLinks = document.querySelectorAll(".nav-link");

    navLinks.forEach(link => {
      link.addEventListener("click", function () {
        // Elimina la clase 'active' de todos los enlaces
        navLinks.forEach(nav => nav.classList.remove("active"));
        // Agrega la clase 'active' al enlace clicado
        this.classList.add("active");
      });
    });
  });

