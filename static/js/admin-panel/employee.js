const matchName = (inputVal) => {
    let i, employeeTable, employeeTableRow, employeeTableId, employeeTableIdVal, 
    employeeTableName, employeeTableNameVal, employeeTableUserName, employeeTableUserNameVal,
    employeeTableRole, employeeTableRoleVal, employeeTableStore, employeeTableStoreVal;

    employeeTable = document.querySelector(".employee__table");
    employeeTableRow = employeeTable.querySelectorAll("tr");

    for (let i=0; i<employeeTableRow.length; i++) {
        employeeTableId = employeeTableRow[i].querySelectorAll("td")[0].querySelector("a");
        employeeTableIdVal = employeeTableId.innerText || employeeTableId.textContent;

        employeeTableName = employeeTableRow[i].querySelectorAll("td")[1].querySelector("a");
        employeeTableNameVal = employeeTableName.innerText || employeeTableId.textContent;

        employeeTableUserName = employeeTableRow[i].querySelectorAll("td")[2].querySelector("a");
        employeeTableUserNameVal = employeeTableUserName.innerText || employeeTableId.textContent;

        employeeTableRole = employeeTableRow[i].querySelectorAll("td")[3].querySelector("a");
        employeeTableRoleVal = employeeTableRole.innerText || employeeTableId.textContent;

        employeeTableStore = employeeTableRow[i].querySelectorAll("td")[4].querySelector("a");
        employeeTableStoreVal = employeeTableStore.innerText || employeeTableId.textContent;

        if (employeeTableIdVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            employeeTableRow[i].style.display = "";
        } else if (employeeTableNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            employeeTableRow[i].style.display = "";
        } else if (employeeTableUserNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            employeeTableRow[i].style.display = "";
        } else if (employeeTableRoleVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            employeeTableRow[i].style.display = "";
        } else if (employeeTableStoreVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            employeeTableRow[i].style.display = "";
        } else {
            employeeTableRow[i].style.display = "none";
        }
    }
}
