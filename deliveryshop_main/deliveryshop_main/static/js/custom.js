let autocomplete;

function initAutoComplete(){
autocomplete = new google.maps.places.Autocomplete(
    document.getElementById('id_address'),
    {   
        types: ['geocode', 'establishment'],
        // added the country that i want to search for
        componentRestrictions: {'country': ['hu']},
    })
// function to specify what should happen when the prediction is clicked
autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged (){
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry){
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    else{
        console.log('place name=>', place.name)
    }

    // get the address components and assign them to the fields
    //console.log(place)
    
    var geocoder = new google.maps.Geocoder()
    var address = document.getElementById('id_address').value

    geocoder.geocode({'address':address}, function(results,status){

        if (status == google.maps.GeocoderStatus.OK) {
            var latitude = results[0].geometry.location.lat();
            var longitude = results[0].geometry.location.lng();

            // jQuery instead of vanilla javascript 
            //updating the values of three HTML input fields with the id attributes of id_latitude, id_longitude, and id_address.
            //this will put the value of this latitude inside the field which has the id of id_latitude
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);

        }

    });
    
    //loop through the address components and assign other address data
    
    //this is the key thing that is helping me to loop and everything
    
    console.log(place.address_components);

    for(var i=0; i < place.address_components.length; i++)
    {
        for(var j=0; j<place.address_components[i].types.length; j++) {

            //get country
            if(place.address_components[i].types[j] == 'country') {
                $('#id_country').val(place.address_components[i].long_name);
            }

            //get state
            if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                $('#id_state').val(place.address_components[i].long_name);
            }
            
            //get city
            if(place.address_components[i].types[j] == 'locality'){
                $('#id_city').val(place.address_components[i].long_name);
            }

            //get pincode
            if(place.address_components[i].types[j] == 'postal_code'){
                $('#id_pincode').val(place.address_components[i].long_name);
            } else {
                $('#id_pincode').val("");
            }      
        }
    }
}

$(document).ready(function() {
    // add to cart
    $('.add_to_cart').on('click',function(e) 
    {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url =$(this).attr('data-url')

        //once it takes the food id, it will send a request to this particular url using the Ajax
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status == 'login_required') {
                    swal(response.message,'','info').then(function() {
                        window.location = '/login';
                    })
                } 
                if (response.status== 'Failed') {
                    swal(response.message,'','error')
                } else {                   
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty); 
                }
            }
        })
    })

    // here placing the cart item quantity on loan
    $('.item_qty').each(function() {
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        $('#' + the_id).html(qty)
    })

    // decreease cart here
    $('.decrease_cart').on('click',function(e) 
    {
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url =$(this).attr('data-url');
        cart_id = $(this).attr('id');

        //once it takes the food id, it will send a request to this particular url using the Ajax
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status == 'login_required') {
                    swal(response.message,'','info').then(function() {
                        window.location = '/login';
                    })
                } else if(response.status == 'Failed') {
                    swal(response.message,'','error')
                } else {                   
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    $('#qty-'+food_id).html(response.qty); 
                    if (window.location.pathname=='/cart/'){
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                }
            }
        })
    })


    // deleting the cart item here
    $('.delete_cart').on('click',function(e) 
    {
        e.preventDefault();

        cart_id = $(this).attr('data-id');
        url =$(this).attr('data-url')

        //once it takes the food id, it will send a request to this particular url using the Ajax
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                console.log(response)
                if(response.status == 'Failed') {
                    swal(response.message,'','error')
                } else {                   
                    $('#cart_counter').html(response.cart_counter['cart_count'])
                    swal(response.status, response.message, "success")
                    removeCartItem(0,cart_id)
                    // check if the cart is empty, i will show the cart is empty message
                    checkEmptyCart();
                }
            }
        })
    })
});


// deleting the cart item if its quantity is 0
function removeCartItem(cart_item_quantity, cart_id){ 
        if (cart_item_quantity<=0){
            // remove the cart item element
            document.getElementById("cart-item-"+cart_id).remove()
        } 
}

// a function that checks if cart is empty
function checkEmptyCart(){
    var cart_counter = document.getElementById('cart_counter').innerHTML
    if (cart_counter == 0){
        document.getElementById("empty-cart").style.display = "block";
    }
}