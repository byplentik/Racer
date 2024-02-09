"use strict";

const updateNumOfItems = (newCount) => {
  $("#num-of-items").text(newCount);
}

const showNotification = (partName) => {
  const cartUrl = $("#notification-data").data("cart-url");
  const toastContainer = $(".toast-container");
  const notification = $(
    '<div class="toast" role="alert" aria-live="assertive" aria-atomic="true">' +
      '<div class="toast-header">' +
      '<strong class="me-auto">Товар успешно добавлен в корзину!</strong>' +
      "</div>" +
      '<div class="toast-body">' +
      "Товар " +
      '<strong style="color: #2cbf2cad;">' +
      partName +
      "</strong>" +
      " успешно был добавлен в корзину" +
      '<div class="mt-2 pt-2 border-top">' +
      '<a href="' +
      cartUrl +
      '"><button type="button" class="btn btn-danger btn-sm">В корзину</button></a>' +
      "</div>" +
      "</div>" +
      "</div>"
  );

  toastContainer.append(notification);

  notification.fadeIn();

  setTimeout(() => {
    notification.fadeOut("slow", function () {
      notification.remove();
    });
  }, 2000);
}

const addToCart = (partId, quantity) => {
  const formData = {
    part_id: partId,
    quantity: quantity,
    csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
  };

  $.ajax({
    type: "POST",
    url: "/cart/add-to-cart/" + partId + "/" + quantity + "/",
    data: formData,
    success: (response) => {
      const newNumOfItems = response.num_items;
      updateNumOfItems(newNumOfItems);

      showNotification(response.part_name);
    },
    error: function (error) {
      alert("Ошибка");
      console.error(error);
    },
  });
}
