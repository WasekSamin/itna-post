// hamburger menu
var hamburger_________id = document.getElementById("hamburger_________id");
const sidebar = document.querySelector("#sidebar");
const closeSidebar = document.querySelector(".sidebar________icon_____close");

hamburger_________id.addEventListener("click", function (e) {
  sidebar.classList.add("show_____menu");
  document
    .querySelector(".admin____overlay")
    .classList.add("show__adminOverlay");
});

closeSidebar.addEventListener("click", () => {
  sidebar.classList.remove("show_____menu");
  document
    .querySelector(".admin____overlay")
    .classList.remove("show__adminOverlay");
});

document.addEventListener("click", (event) => {
  if (event.target.closest("#hamburger_________id")) return;
  if (event.target.closest("#sidebar")) return;

  if (event.target.classList[1] === "show__adminOverlay") {
    document
      .querySelector(".admin____overlay")
      .classList.remove("show__adminOverlay");
  }

  sidebar.classList.remove("show_____menu");
});




const btn = document.querySelector(".logo____save__btn");
btn.style.display = "none";
function foruploadLogo(e) {
  let fileVal = e.files[0].name;

  document.querySelector("#for-shop-name").innerText = fileVal;
  document.querySelector("#for-shop-name").style.display = "flex";
  btn.style.display = "flex";
}