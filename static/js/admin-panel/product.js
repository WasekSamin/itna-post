const matchName = (inputVal) => {
    let i, productTable, productTableRow, productTableId, productId, productIdVal, productTableName, productName, productNameVal, productTableCost, productCost, productCostVal, productTablePrice, productPrice, productPriceVal, productTableStock, productStock, productStockVal;

    productTable = document.querySelector(".prod__table");
    productTableRow = productTable.getElementsByTagName("tr");

    for (i=0; i<productTableRow.length; i++) {
        productTableId = productTableRow[i].getElementsByTagName("td")[0];
        productId = productTableId.getElementsByTagName("a")[0];

        productTableName = productTableRow[i].getElementsByTagName("td")[1];
        productName = productTableName.getElementsByTagName("a")[0];

        productTableCost = productTableRow[i].getElementsByTagName("td")[2];
        productCost = productTableCost.getElementsByTagName("a")[0];

        productTablePrice = productTableRow[i].getElementsByTagName("td")[3];
        productPrice = productTablePrice.getElementsByTagName("a")[0];

        productTableStock = productTableRow[i].getElementsByTagName("td")[4];
        productStock = productTableStock.getElementsByTagName("a")[0];

        productIdVal = productId.innerText || productId.textContent;
        productNameVal = productName.innerText || productName.textContent;
        productCostVal = productCost.innerText || productCost.textContent;
        productPriceVal = productPrice.innerText || productPrice.textContent;
        productStockVal = productStock.innerText || productStock.textContent;

        if (productIdVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            productTableRow[i].style.display = "";
        } else if (productNameVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            productTableRow[i].style.display = "";
        } else if (productCostVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            productTableRow[i].style.display = "";
        } else if (productPriceVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            productTableRow[i].style.display = "";
        } else if (productStockVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
            productTableRow[i].style.display = "";
        } else {
            productTableRow[i].style.display = "none";
        }
    }
}