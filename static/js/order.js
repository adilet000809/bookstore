// JS code to perform AJAX request using jQuery
$(document).ready(function () {
    $('#div_id_address').css('display', 'none');
    $('#id_buy_type').on('click', function () {
        var choice = $(this).val();
        if(choice === 'Delivery'){
            $('#div_id_address').css('display', 'block');
        }
        else{
            $('#div_id_address').css('display', 'none');
        }
    })
});