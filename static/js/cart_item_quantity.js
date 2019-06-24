// JS code to perform AJAX request using jQuery
$(document).ready(function () {
    $('.cart_item_quantity').on('click', function (e) {
        var item = $(this).attr('id');
        var quantity = $(this).val();
        e.preventDefault();
        $.ajax({
            url: '/adjust_cart_item_quantity/',
            data: {
                cart_item_id: item,
                cart_item_quantity: quantity
            },
            dataType: 'json',
            success: function (response) {
                $('#item_price_'+item).text(response.total);
                $('#cart_total').text(response.cart_total)
            }
        });
    });
});