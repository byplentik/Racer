"use strict";

function updateNumOfItems(newCount) {
  $('#num-of-items').text(newCount);
}

function showNotification(partName) {
  var cartUrl = $('#notification-data').data('cart-url');
  var toastContainer = $('.toast-container');
  var notification = $(
    '<div class="toast" role="alert" aria-live="assertive" aria-atomic="true">' +
      '<div class="toast-header">' +
      '<strong class="me-auto">Товар успешно добавлен в корзину!</strong>' +
      '</div>' +
      '<div class="toast-body">' +
        'Товар ' + '<strong style="color: #2cbf2cad;">' + partName + '</strong>' + ' успешно был добавлен в корзину' +
        '<div class="mt-2 pt-2 border-top">' +
        '<a href="' + cartUrl + '"><button type="button" class="btn btn-danger btn-sm">В корзину</button></a>' +
        '</div>' +
      '</div>' +
    '</div>'
  );

    toastContainer.append(notification);

  // Отображение тоста
  notification.fadeIn();

  // Автоматическое скрытие тоста через 2 секунды
  setTimeout(function () {
    notification.fadeOut('slow', function () {
      notification.remove();
    });
  }, 2000);
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
