// Функция отображения всплывающего окна
function showOverlay() {
    document.getElementById('overlay').style.display = 'flex';

    // Добавим обработчик события для закрытия модального окна при клике за его пределами
    document.getElementById('overlay').addEventListener('click', closeModalOnOverlayClick);
}

// Функция скрытия всплывающего окна
function closeModal() {
    document.getElementById('overlay').style.display = 'none';

    // Удалим обработчик события после закрытия модального окна
    document.getElementById('overlay').removeEventListener('click', closeModalOnOverlayClick);
}

// Функция для закрытия модального окна при клике на overlay
function closeModalOnOverlayClick(event) {
    if (event.target.id === 'overlay') {
        closeModal();
    }
}

// Функция обработки выхода
function exit() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', "{% url 'logout' %}", true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

    // Получение CSRF-токена из куки
    var csrftoken = getCookie('csrftoken');
    xhr.setRequestHeader('X-CSRFToken', csrftoken);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Успешный выход - перенаправление на главную страницу
                window.location.href = "{% url 'home' %}";
            } else {
                console.error('Произошла ошибка при выходе:', xhr.statusText);
            }
        }
    };

    xhr.send();
}

// Функция для получения значения куки по имени
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Добавьте обработчик события для кнопки "Выход"
document.getElementById('logout-btn').addEventListener('click', showOverlay);