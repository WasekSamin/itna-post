const advance = document.getElementById("advanceBtn");
const more = document.getElementById("more_____btn");
let btnHide = false;
advance.style.display = "none";

function dropdown() {
  
  if(btnHide){
    advance.style.display = "none";
    btnHide = false;
  }else{
    advance.style.display = "flex";
    btnHide = true;
  }
}

document.addEventListener("click", (event) => {
  if (event.target.closest("#more_____btn")) return;
  if (event.target.closest("#advanceBtn")) return;

  if (event.target.classList[1] === "show__adminOverlay") {
    document
      .querySelector(".admin____overlay")
      .classList.remove("show__adminOverlay");
  }

  advance.style.display = "none";
  btnHide = false;
});
