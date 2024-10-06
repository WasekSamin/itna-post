const matchBrandName = (inputVal) => {
    let i, brandTable, brandTableRow, brandTableData, brandName, brandNameVal;

    brandTable = document.querySelector(".brand__table");
    brandTableRow = brandTable.getElementsByTagName("tr");

    for (let i=0; i<brandTableRow.length; i++) {
        brandTableData = brandTableRow[i].getElementsByTagName("td")[0];

        brandName = brandTableData.querySelector("a");
        brandNameVal = brandName.innerText || brandName.textContent;

        if (brandNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            brandTableRow[i].style.display = "";
        } else {
            brandTableRow[i].style.display = "none";
        }
    }
}