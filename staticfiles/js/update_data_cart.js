"use strict"

function removeFromCart(partId) {
    // Получаем данные формы
    var formData = {
        part_id: partId,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    }

    // Отправляем AJAX-запрос
    $.ajax({
        type: 'POST',
        url: '/cart/remove/' + partId + '/',
        data: formData,
        success: function (response) {
            // Обновление данных в пользовательском интерфейсе, например, обновление суммы и количества товаров в корзине
            updateNumOfItems(response.num_items)
            updateCartUI(response)
        },
        error: function (error) {
            // Обработка ошибок
        }
    })
}

function addToCart(partId) {
    // Получаем данные формы
    var formData = {
        part_id: partId,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
    }

    // Отправляем AJAX-запрос
    $.ajax({
        type: 'POST',
        url: '/cart/add-one-part/' + partId + '/',
        data: formData,
        success: function (response) {
            // Обновление данных в пользовательском интерфейсе
            updateNumOfItems(response.num_items)
            updateCartUI(response)
        },
        error: function (error) {
            // Обработка ошибок
        }
    })
}

function updateCartUI(response) {
    var quantity = response.quantity
    var partId = response.partId
    var total_price = response.total_price
    var num_items = response.num_items

    // Обновляем количество товара в соответствующей ячейке
    var quantityContainer = $('#quantity-' + partId)
    quantityContainer.find('.quantity-value').text(quantity)

    // Если количество товара стало 0, скрываем строку из таблицы
    if (quantity === 0) {
        $('#row-' + partId).hide()
    }

    // Обновляем общую сумму и количество товаров в корзине
    $('#total-price').text('Итого: ' + total_price + ' рублей')
    $('#num-items').text('Всего товаров в корзине: ' + num_items)

    // Проверяем, остались ли еще товары в корзине
    if (num_items === 0) {
        // Скрываем таблицу, кнопки и другие элементы
        $('table, #total-price, #num-items, .hr, .btn-order').hide()
    }
}

// Обработчик клика на кнопке удаления товара
$('body').on('click', '.button-remove-from-cart', function () {
    var partId = $(this).closest('form').data('part-id')
    removeFromCart(partId)
})

// Обработчик клика на кнопке добавления товара
$('body').on('click', '.button-add-to-cart', function () {
    var partId = $(this).closest('form').data('part-id')
    addToCart(partId)
})