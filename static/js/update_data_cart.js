"use strict";

const removeFromCart = (partId) => {
  const formData = {
    part_id: partId,
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
  };

  $.ajax({
    type: "POST",
    url: "/cart/remove/" + partId + "/",
    data: formData,
    success: (response) => {
      updateNumOfItems(response.num_items);
      updateCartUI(response);
    },
    error: (error) => {
      alert("Ошибка");
      console.error(error);
    },
  });
};

const addToCart = (partId) => {
  const formData = {
    part_id: partId,
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
  };

  $.ajax({
    type: "POST",
    url: "/cart/add-one-part/" + partId + "/",
    data: formData,
    success: (response) => {
      updateNumOfItems(response.num_items);
      updateCartUI(response);
    },
    error: (error) => {
      alert("Ошибка");
      console.error(error);
    },
  });
};

const updateCartUI = (response) => {
  const quantity = response.quantity;
  const partId = response.partId;
  const total_price = response.total_price;
  const num_items = response.num_items;

  // Обновляем количество товара в соответствующей ячейке
  const quantityContainer = $("#quantity-" + partId);
  quantityContainer.find(".quantity-value").text(quantity);

  if (quantity === 0) {
    $("#row-" + partId).hide();
  }

  $("#total-price").text("Итого: " + total_price + " рублей");
  $("#num-items").text("Всего товаров в корзине: " + num_items);

  if (num_items === 0) {
    $("table, #total-price, #num-items, .hr, .btn-order").hide();
  }
};

// Обработчик клика на кнопке удаления товара
$("body").on("click", ".button-remove-from-cart", () => {
  const partId = $(this).closest("form").data("part-id");
  removeFromCart(partId);
});

// Обработчик клика на кнопке добавления товара
$("body").on("click", ".button-add-to-cart", () => {
  const partId = $(this).closest("form").data("part-id");
  addToCart(partId);
});
