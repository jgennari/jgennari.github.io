const menuTrigger = document.querySelector("#menu-trigger");
const menu = document.querySelector("#menu");
const mobileNavigation = window.matchMedia("(max-width: 768px)");

if (menuTrigger && menu) {
    const closeMenu = () => {
        menu.classList.add("is-collapsed");
        menuTrigger.setAttribute("aria-expanded", "false");
    };

    const syncMenu = () => {
        if (mobileNavigation.matches) {
            closeMenu();
        } else {
            menu.classList.remove("is-collapsed");
            menuTrigger.setAttribute("aria-expanded", "false");
        }
    };

    menuTrigger.addEventListener("click", (event) => {
        if (!mobileNavigation.matches) {
            return;
        }

        event.stopPropagation();
        const expanded = menuTrigger.getAttribute("aria-expanded") === "true";
        menu.classList.toggle("is-collapsed", expanded);
        menuTrigger.setAttribute("aria-expanded", String(!expanded));
    });

    document.addEventListener("click", (event) => {
        if (mobileNavigation.matches && !menu.contains(event.target)) {
            closeMenu();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && mobileNavigation.matches) {
            closeMenu();
            menuTrigger.focus();
        }
    });

    mobileNavigation.addEventListener("change", syncMenu);
    syncMenu();
}
