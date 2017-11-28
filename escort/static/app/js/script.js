$(document).ready(function () {
    $(".button-collapse").sideNav();
    $('select').material_select();

});
$('.cards').masonry({
    itemSelector: '.card',
    columnWidth: 80
});