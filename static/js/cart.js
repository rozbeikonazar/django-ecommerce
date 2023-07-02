document.addEventListener("DOMContentLoaded", function() {
    var updateBtns = document.getElementsByClassName('update-cart')
  
    for (var i = 0; i < updateBtns.length; i++) {
      updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        if (user === 'AnonymousUser'){

          var registerUrl = document.getElementById('register-link').getAttribute('href');
          window.location.href = registerUrl;
        }
        else {
            
          updateUserOrder(productId, action)
        }
    });
    }
  });
  
  function updateUserOrder(productId, action) {
    var url = '/cart/update_item/';
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
      body: JSON.stringify({ productId: productId, action: action }),
    })
      .then((response) => response.json())
      .then((data) => {
        var quantityElement = document.getElementById('quantity_' + productId);
        quantityElement.innerText = data.quantity;
  
        var totalElement = document.getElementById('total_' + productId);
        totalElement.innerText = data.total;
  
        var cartItemsElement = document.getElementById('cart-items');
        cartItemsElement.innerText = data.cart_items;
  
        var cartTotalElement = document.getElementById('cart-total');
        cartTotalElement.innerText = data.cart_total;
      });
  }
  