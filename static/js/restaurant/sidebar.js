const restaurantHamburgerMenu = document.querySelector(".restaurant__hamburgerMenu");
const restaurantSidebar = document.querySelector("#restaurant__sidebar");
const closeRestaurantSidebar = document.querySelector(".close__restaurant__sidebar");
const restaurantOverlay = document.querySelector(".restaurant__overlay");

restaurantHamburgerMenu.addEventListener("click", () => {
    restaurantSidebar.classList.add("show__restaurantSidebar");
    restaurantOverlay.classList.add("show__restaurantOverlay");
});

closeRestaurantSidebar.addEventListener("click", () => {
    restaurantSidebar.classList.remove("show__restaurantSidebar");
    restaurantOverlay.classList.remove("show__restaurantOverlay");
});

document.addEventListener("click", (event) => {
    if (event.target.closest(".restaurant__hamburgerMenu")) return;
    if (event.target.closest("#restaurant__sidebar")) return;

    restaurantSidebar.classList.remove("show__restaurantSidebar");
    restaurantOverlay.classList.remove("show__restaurantOverlay");
});

