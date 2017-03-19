$(document).ready(function () {
    $('select').material_select();
});

$('.js-create-note').on('submit', function (e) {
    e.preventDefault();

    var answers_ids = [];
    $.each($('select'), function () {
        answers_ids.push($(this).val());
    });

    var data = $(this).serialize();
    data += '&answers_ids=' + JSON.stringify(answers_ids);

    $.post(location.pathname, data).success(function (data) {
        location.pathname = '/';
    }).error(function (e) {
        alert('Ошибка, попробуйте еще раз')
    })
});