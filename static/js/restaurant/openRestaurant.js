// cash change js
const reciveCash = document.getElementById("received__cash");
const amountReceived = document.getElementById("amount_received");
const hiddenInput = document.getElementById("restaurantTotalAmount");
const change = document.getElementById("change");

function cashOnekChash() {
  const takenInput = reciveCash.value;
  const showTakenInput = (amountReceived.innerHTML = takenInput);
  if (hiddenInput) {
    let hiddenInputVal = hiddenInput.value;
    const changeAmount = hiddenInputVal - showTakenInput;
    const finalChange = (change.innerHTML = changeAmount);
  }

  if (!takenInput) {
    change.innerHTML = 0;
  }
}

const matchName = (inputVal) => {
  let i, j, k, l, restaurantMiddleContent, restaurantRightCatSection, 
  restuarantProductCard, restaurantCatName, restaurantCatNameVal,
  restaurantProductName, restaurantProductNameVal;
  let x = [], y = []; // x -> product_name, y => category_name

  restaurantMiddleContent = document.querySelector(".restaurant__rightMiddleContent ");
  restaurantRightCatSection = restaurantMiddleContent.querySelectorAll(".restaurant__rightCategorySection");
  
  for (i=0; i<restaurantRightCatSection.length; i++) {
    restaurantCatName = restaurantRightCatSection[i].querySelector(".restaurant__catName");
    restaurantCatNameVal = restaurantCatName.innerText || restaurantCatName.textContent;
    
    if (restaurantCatNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
      y.push(restaurantRightCatSection[i]);
    } else {
      restaurantRightCatSection[i].style.display = "none";
    }

    restuarantProductCard = restaurantRightCatSection[i].querySelectorAll(".restaurant__rightProductCard");

    
    for (j=0; j<restuarantProductCard.length; j++) {
      restaurantProductName = restuarantProductCard[j].querySelector(".get__restaurantProductName");
      restaurantProductNameVal = restaurantProductName.innerText || restaurantProductName.textContent;

      if (restaurantProductNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
        x.push(restuarantProductCard[j]);
        y.push(restaurantRightCatSection[i]);
      } else {
        restuarantProductCard[j].style.display = "none";
      }
    }

    if (y.length > 0) {
      for (k=0; k<y.length; k++) {
        if (x.length > 0) {
          for (l=0; l<x.length; l++) {
            y[k].style.display = "";
            x[l].style.display = "";
          }
        } else {
          for (j=0; j<restuarantProductCard.length; j++) {
            restuarantProductCard[j].style.display = "";
          }
        }
      }
    }
  }
}

const restaurantCashButton = document.querySelector(".restaurant__cashButton");
const restaurantCashModel = document.querySelector(".restaurant__cashModal");
const restaurantModalOverlay = document.querySelector(
  "#restaurant__modalOverlay"
);
const closeRestaurantCashModal = document.querySelector(
  "#close__restaurantModal"
);
const restaurantWalkinOption = document.querySelector(".restaurant__walkIn");
const restaurantCustomerList = document.querySelector(
  ".restaurant__CustomerList"
);
const restaurantAddNewCustomer = document.querySelector(
  "#restaurant__addNewCustomer"
);
const restaurantAddNewCustomerForm = document.querySelector(
  "#restaurant__addNewCustomerForm"
);

const getCustomer = document.querySelector("#get_customer");

restaurantCashButton.addEventListener("click", () => {
  restaurantCashModel.classList.add("show__restaurantCashModal");
  restaurantModalOverlay.classList.add("show__restaurantModalOverlay");
});

closeRestaurantCashModal.addEventListener("click", () => {
  restaurantCashModel.classList.remove("show__restaurantCashModal");
  restaurantModalOverlay.classList.remove("show__restaurantModalOverlay");
});

restaurantWalkinOption.addEventListener("click", () => {
  restaurantCustomerList.classList.add("show__resstaurantCustomerList");
});

restaurantAddNewCustomer.addEventListener("click", () => {
  restaurantAddNewCustomerForm.classList.add(
    "show__restaurantAddNewCustomerForm"
  );
});

document.addEventListener("click", (event) => {
  // console.log(event.target);
  if (event.target.closest(".restaurant__cashButton")) return;
  if (event.target.closest(".restaurant__cashModal")) return;
  if (event.target.closest(".restaurant__walkIn")) return;
  if (event.target.closest(".restaurant__CustomerList")) return;
  if (event.target.closest("#restaurant__addNewCustomer")) return;

  if (event.target.id === "restaurant__modalOverlay") {
    restaurantCashModel.classList.remove("show__restaurantCashModal");
    restaurantCustomerList.classList.remove("show__resstaurantCustomerList");
    restaurantModalOverlay.classList.remove("show__restaurantModalOverlay");
    return;
  }

  restaurantCustomerList.classList.remove("show__resstaurantCustomerList");
  restaurantAddNewCustomerForm.classList.remove(
    "show__restaurantAddNewCustomerForm"
  );
});

// console.log(getCustomer.value);

const selectedCustomer = (e) => {
  // console.log(e.id);
  const custId = e.id.split("-")[1];
  const username = e.id.split("-")[2];

  document.getElementById("getCustomerWalkIn").innerHTML =
    username +
    ' <span class="iconify" data-icon="akar-icons:chevron-down"></span>';
  document.getElementById("get_customer_id").value = custId;
};

const selectWalkIn = (e) => {
  document.getElementById("getCustomerWalkIn").innerHTML =
    "Walk-In" +
    ' <span class="iconify" data-icon="akar-icons:chevron-down"></span>';
  document.getElementById("get_customer_id").value = "";
};
