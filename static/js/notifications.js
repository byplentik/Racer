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
    notification.fadeOut("slow", () => {
      notification.remove();
    });
  }, 2000);
};
