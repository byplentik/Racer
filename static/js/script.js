"use strict";

function updateNumOfItems(newCount) {
  $('#num-of-items').text(newCount);
}

function showNotification(partName) {
  var notification = $('<div class="notification">Товар ' + partName + ' успешно был добавлен в корзину</div>');

  $('body').append(notification);

  setTimeout(function () {
    notification.fadeOut('slow', function () {
      notification.remove();
    });
  }, 1000); 
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
      var newNumOfItems = response.num_items;
      updateNumOfItems(newNumOfItems);

      showNotification(response.part_name);
    },
    error: function (error) {
      // Обработка ошибок
    }
  });
}
