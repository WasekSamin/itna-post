const matchName = (inputVal) => {
    let i, adminOrderTable, adminOrderTableRow, 
    adminCreatedAt, adminCreatedAtVal, adminOrderId, adminOrderIdVal,
    adminSubmissionDate, adminSubmissionDateVal, adminDueTotal, adminDueTotalVal,
    adminOrderNote, adminOrderNoteVal;

    adminOrderTable = document.querySelector(".admin__orderTable");
    adminOrderTableRow = adminOrderTable.querySelectorAll("tr");

    for (i=0; i<adminOrderTableRow.length; i++) {
        adminCreatedAt = adminOrderTableRow[i].getElementsByTagName("td")[0].querySelector("a");
        adminCreatedAtVal = adminCreatedAt.innerText || adminCreatedAt.textContent;
        
        adminOrderId = adminOrderTableRow[i].getElementsByTagName("td")[2].querySelector("a");
        adminOrderIdVal = adminOrderId.innerText || adminOrderId.textContent;

        adminSubmissionDate = adminOrderTableRow[i].getElementsByTagName("td")[3].querySelector("a");
        adminSubmissionDateVal = adminSubmissionDate.innerText || adminSubmissionDate.textContent;

        adminDueTotal = adminOrderTableRow[i].getElementsByTagName("td")[4].querySelector("a");
        adminDueTotalVal = adminDueTotal.innerText || adminDueTotal.textContent;

        adminOrderNote = adminOrderTableRow[i].getElementsByTagName("td")[5].querySelector("a");
        adminOrderNoteVal = adminOrderNote.innerText || adminOrderNote.textContent;
        
        if (adminCreatedAtVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminOrderIdVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminSubmissionDateVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminDueTotalVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else if (adminOrderNoteVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            adminOrderTableRow[i].style.display = "";
        } else {
            adminOrderTableRow[i].style.display = "none";
        }
    }
}