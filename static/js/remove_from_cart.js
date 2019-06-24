// JS code to perform AJAX request using jQuery
$(document).ready(function () {
    $('.remove_from_cart').on('click', function (e) {
        var item = $(this).attr('id');
        e.preventDefault();
        $.ajax({
            url: '/remove_from_cart_view/',
            data: {
                cart_item_id: item,
            },
            dataType: 'json',
            success: function (response) {
                $('.cart_item_'+item).css('display', 'none');
                $('.cart_count').text(response.count);
                $('#cart_total').text(response.cart_total);
                if(parseInt(response.cart_total)===0){
                    $('#cart_empty').text('Your cart is empty.');
                    $('#empty').css('display', 'none');
                }
            }
        });
    });
});