let shopLogoImg = document.getElementById("shop__logoImg");

const getShopLogo = (e) => {
    let imgFile = e.files[0];

    if (imgFile) {
        shopLogoImg.src = URL.createObjectURL(imgFile);
        shopLogoImg.style.display = "inherit";
    }
}