$('.js-create-note').on('submit', function (e) {
    e.preventDefault();
    $.post(location.pathname, $(this).serialize()).success(function (data) {
        location.reload();
    }).error(function (e) {
        alert('Ошибка, попробуйте еще раз')
    });

});