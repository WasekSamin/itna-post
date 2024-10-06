function matchName(inputVal) {
    var restaurantPaymentCustName, restaurantPaymentTable, restaurantPaymentRow, restaurantPaymentOrderId, i, usernameVal, orderIdVal, restaurantGrandTotal, restaurantChange, restaurantDiscount, restuarantOrderDate, dateVal, grandTotalVal, changeVal, discountVal;
    restaurantPaymentTable = document.querySelector(".restaurant__allPaymentOrdersTable");
    restaurantPaymentRow = restaurantPaymentTable.getElementsByTagName("tr");
    for (i = 0; i < restaurantPaymentRow.length; i++) {
        restaurantPaymentCustName = document.getElementsByClassName("restaurant__paymentCustName")[i];
        restaurantPaymentOrderId = document.getElementsByClassName("restaurant__paymentOrderId")[i];
        restaurantGrandTotal = document.getElementsByClassName("restaurant__grandTotal")[i];
        restaurantChange = document.getElementsByClassName("restaurant__change")[i];
        restaurantDiscount = document.getElementsByClassName("restaurant__discount")[i];
        restuarantOrderDate = document.getElementsByClassName("restaurant__orderDate")[i];

        dateVal = restuarantOrderDate.innerText || restuarantOrderDate.textContent;
        usernameVal = restaurantPaymentCustName.innerText || restaurantPaymentCustName.textContent;
        orderIdVal = restaurantPaymentOrderId.innerText || restaurantPaymentOrderId.textContent;
        grandTotalVal = restaurantGrandTotal.iinnerText || restaurantGrandTotal.textContent;
        changeVal = restaurantChange.innerText || restaurantChange.textContent;
        discountVal = restaurantDiscount.innerText || restaurantChange.textContent;

        if (dateVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            restaurantPaymentRow[i].style.display = "";
        }
        else if (usernameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            restaurantPaymentRow[i].style.display = "";
        } else if (orderIdVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            restaurantPaymentRow[i].style.display = "";
        } else if (grandTotalVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            restaurantPaymentRow[i].style.display = "";
        } else if (changeVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            restaurantPaymentRow[i].style.display = "";
        } else if (discountVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            restaurantPaymentRow[i].style.display = "";
        } else {
            restaurantPaymentRow[i].style.display = "none";
        }
    }
}