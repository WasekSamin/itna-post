const matchName = (inputVal) => {
    let i, adminOrderTable, adminOrderTableRow, 
    adminCustomerName, adminCustomerNameVal, adminCustomerPhone, adminCustomerPhoneVal,
    adminTable, adminTableVal, adminStatus, adminStatusVal, adminAmount, adminAmountVal,
    adminChange, adminChangeVal, adminTotal, adminTotalVal, adminShop, adminShopVal;

    adminOrderTable = document.querySelector(".admin__orderTable");
    adminOrderTableRow = adminOrderTable.querySelectorAll("tr");

    for (i=0; i<adminOrderTableRow.length; i++) {
        adminCustomerName = adminOrderTableRow[i].getElementsByTagName("td")[0].querySelector("a");
        adminCustomerNameVal = adminCustomerName.innerText || adminCustomerName.textContent;
        
        adminCustomerPhone = adminOrderTableRow[i].getElementsByTagName("td")[1].querySelector("a");
        adminCustomerPhoneVal = adminCustomerPhone.innerText || adminCustomerPhone.textContent;

        adminTable = adminOrderTableRow[i].getElementsByTagName("td")[2].querySelector("a");
        adminTableVal = adminTable.innerText || adminTable.textContent;

        adminStatus = adminOrderTableRow[i].getElementsByTagName("td")[3].querySelector("a");
        adminStatusVal = adminStatus.innerText || adminStatus.textContent;

        adminAmount = adminOrderTableRow[i].getElementsByTagName("td")[4].querySelector("a");
        adminAmountVal = adminAmount.innerText || adminAmount.textContent;

        adminChange = adminOrderTableRow[i].getElementsByTagName("td")[5].querySelector("a");
        adminChangeVal = adminChange.innerText || adminChange.textContent;

        adminTotal = adminOrderTableRow[i].getElementsByTagName("td")[6].querySelector("a");
        adminTotalVal = adminTotal.innerText || adminTotal.textContent;

        adminShop = adminOrderTableRow[i].getElementsByTagName("td")[7].querySelector("a");
        adminShopVal = adminShop.innerText || adminShop.textContent;
        
        if (adminCustomerNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminCustomerPhoneVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminTableVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminStatusVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminAmountVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminChangeVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminTotalVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminShopVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else {
            adminOrderTableRow[i].style.display = "none";
        }
    }
}