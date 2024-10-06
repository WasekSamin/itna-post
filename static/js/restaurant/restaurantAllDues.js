const matchName = (inputVal) => {
    let i, allDueTable, allTableRow, tableCreatedAtData, createdAt, createdAtVal, tableOrderIdData, orderId, orderIdVal, tableSubmissionData, submissionDate, submissionDateVal, tableDueData, dueData, dueDataVal, tableOrderNote, orderNote, orderNoteVal;

    allDueTable = document.querySelector(".restaurant__allPaymentDueTable");
    allTableRow = allDueTable.querySelectorAll("tr");

    for (i=0; i<allTableRow.length; i++) {
        tableCreatedAtData = allTableRow[i].getElementsByTagName("td")[0];
        createdAt = tableCreatedAtData.querySelector("a");

        tableOrderIdData = allTableRow[i].getElementsByTagName("td")[2];
        orderId = tableOrderIdData.querySelector("a");

        tableSubmissionData = allTableRow[i].getElementsByTagName("td")[3];
        submissionDate = tableSubmissionData.querySelector("a");

        tableDueData = allTableRow[i].getElementsByTagName("td")[4];
        dueData = tableDueData.querySelector("a");

        tableOrderNote = allTableRow[i].getElementsByTagName("td")[5];
        orderNote = tableOrderNote.querySelector("a");

        createdAtVal = createdAt.innerText || createdAt.textContent;
        orderIdVal = orderId.innerText || orderId.textContent;
        submissionDateVal = submissionDate.innerText || submissionDate.textContent;
        dueDataVal = dueData.innerText || dueData.textContent;
        orderNoteVal = orderNote.innerText || orderNote.textContent;

        if (createdAtVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            allTableRow[i].style.display = "";
        } else if (orderIdVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            allTableRow[i].style.display = "";
        } else if (submissionDateVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            allTableRow[i].style.display = "";
        } else if (dueDataVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            allTableRow[i].style.display = "";
        } else if (orderNoteVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            allTableRow[i].style.display = "";
        } else {
            allTableRow[i].style.display = "none";
        }
    }
}