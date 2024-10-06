const matchName = (inputVal) => {
    let i, customerTable, customerTableRow, customerTableName, customerName, customerNameVal, customerTableEmail, customerEmail, customerEmailVal, customerTableMobile, customerMobile, customerMobileVal;

    customerTable = document.querySelector(".customer__table");
    customerTableRow = customerTable.getElementsByTagName("tr");

    for (let i=0; i<customerTableRow.length; i++) {
        customerTableName = customerTableRow[i].getElementsByTagName("td")[0];
        customerName = customerTableName.querySelector("a");

        customerTableEmail = customerTableRow[i].getElementsByTagName("td")[1];
        customerEmail = customerTableEmail.querySelector("a");

        customerTableMobile = customerTableRow[i].getElementsByTagName("td")[2];
        customerMobile = customerTableMobile.querySelector("a");

        customerNameVal = customerName.innerText || customerName.textContent;
        customerEmailVal = customerEmail.innerText || customerEmail.textContent;
        customerMobileVal = customerMobile.innerText || customerMobile.textContent;

        if (customerNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            customerTableRow[i].style.display = "";
        } else if (customerEmailVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            customerTableRow[i].style.display = "";
        } else if (customerMobileVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            customerTableRow[i].style.display = "";
        } else {
            customerTableRow[i].style.display = "none";
        }
    }

}