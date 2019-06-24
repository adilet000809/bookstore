// JS code to perform AJAX request using jQuery
$(document).ready(function () {
    $('.cart').on('click', function (e) {
        var slug = $(this).attr('id');
        // Prevent page refresh
        e.preventDefault();
        $.ajax({
            url: '/add_to_cart/',
            data: {
                product_slug: slug,
            },
            dataType: 'json',
            success: function (response) {
                $('.cart_response').text('The item '+response.product+' has been added to your cart. Quantity: '+response.quantity);
            }
        });
    });
});