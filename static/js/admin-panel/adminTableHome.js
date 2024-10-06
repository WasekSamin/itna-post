const matchName = (inputVal) => {
    let i, allTable, allTableRow, tableNameData, tableName, tableNameVal, tableWaiterData, tableWaiter, tableWaiterVal;

    allTable = document.querySelector(".allTable__table");
    allTableRow = allTable.querySelectorAll("tr");

    for (i=0; i<allTableRow.length; i++) {
        tableNameData = allTableRow[i].getElementsByTagName("td")[0];
        tableName = tableNameData.querySelector("a");

        tableNameVal = tableName.innerText || tableName.textContent;

        tableWaiterData = allTableRow[i].getElementsByTagName("td")[2];
        tableWaiter = tableWaiterData.querySelector("a");

        tableWaiterVal = tableWaiter.innerText || tableWaiter.textContent;

        if (tableNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            allTableRow[i].style.display = "";
        } else if (tableWaiterVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            allTableRow[i].style.display = "";
        } else {
            allTableRow[i].style.display = "none";
        }
    }
}