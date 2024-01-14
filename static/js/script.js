"use strict"

function updateNumOfItems(newCount) {
  $('#num-of-items').text(newCount);
}

function addToCart(partId, quantity) {
  // Получаем данные формы
  var formData = {
    'part_id': partId,
    'quantity': quantity,
    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
  };

  // Отправляем AJAX-запрос
  $.ajax({
    type: 'POST',
    url: '/cart/add-to-cart/' + partId + '/' + quantity + '/',
    data: formData,
    success: function (response) {
      // Обновляем значение переменной get_num_of_items
      var newNumOfItems = response.num_items
      updateNumOfItems(newNumOfItems);
    },
    error: function (error) {
      // Обработка ошибок
    }
  });

  var partName = getPartName(partId); // Assuming you have a function to get the part name
  showNotification('Product ' + partName + ' was successfully added to cart');
}


function showNotification(message) {
  var notification = document.createElement('div');
  notification.className = 'notification';
  notification.innerHTML = message;

  document.body.appendChild(notification);

  // Auto-hide the notification after a few seconds
  setTimeout(function () {
    document.body.removeChild(notification);
  }, 3000); // Adjust the time as needed
}

function getPartName(partId) {
  // Implement this function to fetch the part name based on partId
  // You can make an AJAX request or use any other method to get the name
  // For simplicity, you can return a static value for now.
  return 'Example Part';
}