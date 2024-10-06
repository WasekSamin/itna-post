const matchName = (inputVal) => {
    let i, adminOrderTable, adminOrderTableRow, 
    adminDate, adminDateVal, adminCustomerName, adminCustomerNameVal,
    adminNumPeople, adminNumPeopleVal, adminAmount, adminAmountVal,
    adminMethod, adminMethodVal;

    adminOrderTable = document.querySelector(".admin__orderTable");
    adminOrderTableRow = adminOrderTable.querySelectorAll("tr");

    for (i=0; i<adminOrderTableRow.length; i++) {
        adminDate = adminOrderTableRow[i].getElementsByTagName("td")[0].querySelector("a");
        adminDateVal = adminDate.innerText || adminDate.textContent;
        
        adminCustomerName = adminOrderTableRow[i].getElementsByTagName("td")[1].querySelector("a");
        adminCustomerNameVal = adminCustomerName.innerText || adminCustomerName.textContent;

        adminNumPeople = adminOrderTableRow[i].getElementsByTagName("td")[2].querySelector("a");
        adminNumPeopleVal = adminNumPeople.innerText || adminNumPeople.textContent;

        adminAmount = adminOrderTableRow[i].getElementsByTagName("td")[3].querySelector("a");
        adminAmountVal = adminAmount.innerText || adminAmount.textContent;

        adminMethod = adminOrderTableRow[i].getElementsByTagName("td")[4].querySelector("a");
        adminMethodVal = adminMethod.innerText || adminMethod.textContent;
        
        if (adminDateVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminCustomerNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminNumPeopleVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminAmountVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminMethodVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else {
            adminOrderTableRow[i].style.display = "none";
        }
    }
}