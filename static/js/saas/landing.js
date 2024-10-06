// back to top
const toTop = document.querySelector(".to-top");

window.addEventListener("scroll", () => {
  if (window.pageYOffset > 100) {
    toTop.classList.add("back-to-top");
  } else {
    toTop.classList.remove("back-to-top");
  }
})


// infinite typin
var typed = new Typed ('.type-animate', {
    strings: [
      "POS Software Provider",
      "POS Software Provider",
      "CRM Software Provider"
    ],
    typeSpeed: 50,
    backSpeed: 50,
    loop: true
});


// hamburger menu
var hamburger_________id = document.getElementById("hamburger_________id");
const sidebar = document.querySelector("#sidebar");
const closeSidebar = document.querySelector(".sidebar________icon_____close");

hamburger_________id.addEventListener("click", function(e) {
    sidebar.classList.add("show_____menu");
});

closeSidebar.addEventListener("click", () => {
  sidebar.classList.remove("show_____menu");
});

document.addEventListener("click", (event) => {
  if (event.target.closest("#hamburger_________id")) return;
  if (event.target.closest("#sidebar")) return;

  sidebar.classList.remove("show_____menu");
})



// slider

$('.owl-carousel').owlCarousel({
  loop:true,
  responsive:{
      0:{
          items:1
      },
      600:{
          items:2
      },
      1000:{
          items:3
      }
  }
})