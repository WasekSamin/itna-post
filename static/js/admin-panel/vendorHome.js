const matchName = (inputVal) => {
    let i, vendorTable, vendorTableRow, vendorTableName, vendorTableTaxId, vendorTableShop, vendorName, vendorNameVal, vendorTax, vendorTaxVal, vendorShop, vendorShopVal;

    vendorTable = document.querySelector(".vendor__table");
    vendorTableRow = vendorTable.querySelectorAll("tr");

    for (i=0; i<vendorTableRow.length; i++) {
        vendorTableName = vendorTableRow[i].getElementsByTagName("td")[0];
        vendorTableTaxId = vendorTableRow[i].getElementsByTagName("td")[1];
        vendorTableShop = vendorTableRow[i].getElementsByTagName("td")[2];

        vendorName = vendorTableName.querySelector("a");
        vendorTax = vendorTableTaxId.querySelector("a");
        vendorShop = vendorTableShop.querySelector("a");

        vendorNameVal = vendorName.innerText || vendorName.textContent;
        vendorTaxVal = vendorTax.innerText || vendorTax.textContent;
        vendorShopVal = vendorShop.innerText || vendorShop.textContent;

        if (vendorNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            vendorTableRow[i].style.display = "";
        } else if (vendorTaxVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            vendorTableRow[i].style.display = "";
        } else if (vendorShopVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            vendorTableRow[i].style.display = "";
        } else {
            vendorTableRow[i].style.display = "none";
        }
    }
}