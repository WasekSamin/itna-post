const matchName = (inputVal) => {
    let i, adminOrderTable, adminOrderTableRow, adminOrderIdData, adminOrderId, adminOrderIdVal, adminCreatedData, adminCreated, adminCreatedVal, adminPaymentData, adminPayment, adminPaymentVal, adminTotalSaleData, adminTotalSale, adminTotalSaleVal, adminSoldUserData, adminSoldUser, adminSoldUserVal, adminCustomerData, adminCustomer, adminCustomerVal;

    adminOrderTable = document.querySelector(".admin__orderTable");
    adminOrderTableRow = adminOrderTable.querySelectorAll("tr");

    for (let i=0; i<adminOrderTableRow.length; i++) {
        adminOrderIdData = adminOrderTableRow[i].getElementsByTagName("td")[0];
        adminOrderId = adminOrderIdData.querySelector("a");

        adminCreatedData = adminOrderTableRow[i].getElementsByTagName("td")[1];
        adminCreated = adminCreatedData.querySelector("a");

        adminPaymentData = adminOrderTableRow[i].getElementsByTagName("td")[2];
        adminPayment = adminPaymentData.querySelector("a");

        adminTotalSaleData = adminOrderTableRow[i].getElementsByTagName("td")[3];
        adminTotalSale = adminTotalSaleData.querySelector("a");

        adminSoldUserData = adminOrderTableRow[i].getElementsByTagName("td")[4];
        adminSoldUser = adminSoldUserData.querySelector("a");

        adminCustomerData = adminOrderTableRow[i].getElementsByTagName("td")[5];
        adminCustomer = adminCustomerData.querySelector("a");

        adminOrderIdVal = adminOrderId.innerText || adminOrderId.textContent;
        adminCreatedVal = adminCreated.innerText || adminCreated.textContent;
        adminPaymentVal = adminPayment.innerText || adminPayment.textContent;
        adminTotalSaleVal = adminTotalSale.innerText || adminTotalSale.textContent;
        adminSoldUserVal = adminSoldUser.innerText || adminSoldUser.textContent;
        adminCustomerVal = adminCustomer.innerText || adminCustomer.textContent;

        if (adminOrderIdVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminCreatedVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminPaymentVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminTotalSaleVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminSoldUserVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminCustomerVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else {
            adminOrderTableRow[i].style.display = "none";
        }
    }
}