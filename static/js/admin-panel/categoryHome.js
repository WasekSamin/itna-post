const matchCatName = (inputVal) => {
  let i, categoryTable, categoryRow, categoryName, categoryData, catVal;

  categoryTable = document.querySelector(".catgory__table");
  categoryRow = categoryTable.getElementsByTagName("tr");

  for (let i = 0; i < categoryRow.length; i++) {
    categoryData = document.querySelectorAll(".category__data")[i];
    // console.log(categoryData);
    categoryName = categoryData.querySelector(".category__name");

    catVal = categoryName.innerText || categoryName.textContent;

    if (catVal.toLowerCase().indexOf(inputVal.value.toLowerCase()) > -1) {
        categoryRow[i].style.display = "";
    } else {
        categoryRow[i].style.display = "none";
    }
  }
};
