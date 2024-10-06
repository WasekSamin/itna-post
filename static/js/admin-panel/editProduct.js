const shopId = document.getElementById("get__shopId");

const getCategory = (e) => {
    if (e.value === "add-category") {
        window.location.href = `/adminpanel/create-category/${shopId.value}/`;
    }
}


const getBrand = (e) => {
    if (e.value === "add-brand"){
        window.location.href = `/adminpanel/create-brand/${shopId.value}/`;
    }
}


// for create product
const shopIdCreate = document.getElementById("get__shopId__create");

const createCategory = (e) => {
    if (e.value === "add-category") {
        window.location.href = `/adminpanel/create-category/${shopIdCreate.value}/`;
    }
}


const createBrand = (e) => {
    if (e.value === "add-brand"){
        window.location.href = `/adminpanel/create-brand/${shopIdCreate.value}/`;
    }
}
