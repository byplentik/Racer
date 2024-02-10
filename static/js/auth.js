const exit = () => {
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "{% url 'logout' %}", true);
  xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");

  const csrftoken = getCookie("csrftoken");
  xhr.setRequestHeader("X-CSRFToken", csrftoken);

  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        window.location.href = "{% url 'home' %}";
      } else {
        console.error("Произошла ошибка при выходе:", xhr.statusText);
      }
    }
  };

  xhr.send();
};

if (document.getElementById("logout-btn")) {
  document.getElementById("logout-btn").addEventListener("click", showOverlay);
}
