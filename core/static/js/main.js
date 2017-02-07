$(document).ready(function () {
    $('select').material_select();
});

$('.js-form-submit').submit(function (e) {
    e.preventDefault();
    var result_mark = 0;
    $.each($('select'), function (index, el) {
        if (!$(el).val()) {
            alert('заполните все поля');
            result_mark = undefined;
            return false;
        } else {
            result_mark += $(el).val()
        }
    });
    if (result_mark <= 7) {
        alert('(легкая симптоматика) – пациенту показано дальнейшее наблюдение, возможно назначение симптоматической терапии');
    } else if (result_mark >= 8 && result_mark <= 19) {
        alert('(умеренная степень тяжести) – пациенту показано дообследование с целью подбора препаратов для консервативного лечения');
    } else if (result_mark >= 20) {
        alert('(тяжелая степень нарушений) – пациенту показано комплексное урологическое обследование, рекомендуется оперативное лечение');
    }
});