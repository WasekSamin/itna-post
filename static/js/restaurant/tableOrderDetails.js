const matchName = (inputVal) => {
    let i, tableOrders, tableOrderRow, tableCustomerName, tableCustomerNameVal,
    tableCustomerPhone, tableCustomerPhoneVal, tableTable, tableTableVal,
    tableStatus, tableStatusVal, tableAmount, tableAmountVal, tableChange, tableChangeVal, 
    tableTotal, tableTotalVal, tableShop, tableShopVal;

    tableOrders = document.querySelector(".table__tableOrders");
    tableOrderRow = tableOrders.querySelectorAll("tr");

    for (i=0; i<tableOrderRow.length; i++) {
        tableCustomerName = tableOrderRow[i].querySelectorAll("td")[0].querySelector("a");
        tableCustomerNameVal = tableCustomerName.innerText || tableCustomerName.textContent;

        tableCustomerPhone = tableOrderRow[i].querySelectorAll("td")[1].querySelector("a");
        tableCustomerPhoneVal = tableCustomerPhone.innerText || tableCustomerPhone.textContent;

        tableTable = tableOrderRow[i].querySelectorAll("td")[2].querySelector("a");
        tableTableVal = tableTable.innerText || tableTable.textContent;

        tableStatus = tableOrderRow[i].querySelectorAll("td")[3].querySelector("a");
        tableStatusVal = tableStatus.innerText || tableStatus.textContent;

        tableAmount = tableOrderRow[i].querySelectorAll("td")[4].querySelector("a");
        tableAmountVal = tableAmount.innerText || tableAmount.textContent;

        tableChange = tableOrderRow[i].querySelectorAll("td")[5].querySelector("a");
        tableChangeVal = tableChange.innerText || tableChange.textContent;

        tableTotal = tableOrderRow[i].querySelectorAll("td")[6].querySelector("a");
        tableTotalVal = tableTotal.innerText || tableTotal.textContent;

        tableShop = tableOrderRow[i].querySelectorAll("td")[7].querySelector("a");
        tableShopVal = tableShop.innerText || tableShop.textContent;
        

        if (tableCustomerNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            tableOrderRow[i].style.display = "";
        } else if (tableCustomerPhoneVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            tableOrderRow[i].style.display = "";
        } else if (tableTableVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            tableOrderRow[i].style.display = "";
        } else if (tableStatusVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            tableOrderRow[i].style.display = "";
        } else if (tableAmountVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            tableOrderRow[i].style.display = "";
        } else if (tableChangeVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            tableOrderRow[i].style.display = "";
        } else if (tableTotalVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            tableOrderRow[i].style.display = "";
        } else if (tableShopVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            tableOrderRow[i].style.display = "";
        } else {
            tableOrderRow[i].style.display = "none";
        }
    }
}