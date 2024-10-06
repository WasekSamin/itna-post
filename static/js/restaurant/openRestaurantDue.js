window.onload = function(){
    const restaurantLeftNavbar = document.querySelector(".restaurant__leftNavbar");
    const gobackToHome = document.getElementById("goBackToHome").value;
    const restaurantLeftButtons = document.querySelectorAll(".restaurant__leftFormButtons");

    restaurantLeftNavbar.innerHTML = `<div>
        <a class="d-flex align-items-center text-white" href="/restaurant/open-restaurant/${gobackToHome}" class="text-white">
            <span class="iconify fs-5" data-icon="ant-design:left-outlined"></span> Back
        </a>
    </div>`

    console.log(restaurantLeftButtons);
    for (let i=0; i<restaurantLeftButtons.length; i++) {
        console.log(restaurantLeftButtons[i]);
        restaurantLeftButtons[i].style.setProperty("display", "none", "important");
    }
}

$(document).ready(function() {
    $("#calendar").datepicker({
        onSelect: function() {
            let dateObject = $(this).datepicker();

            if (dateObject) {
                $("#calendar").val(dateObject.val());
            }
        }
    });
});