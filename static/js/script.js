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
      success: function(response) {
        // Обновляем значение переменной get_num_of_items
        var newNumOfItems = response.num_items
        updateNumOfItems(newNumOfItems);
      },
      error: function(error) {
        // Обработка ошибок
      }
    });
  }
