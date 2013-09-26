/**
 * Selects color
 */
function selectColor(el) {
    var color_id = $(el).data('value');
    console.log(color_id);
    // Select color
    $('#id_color').val(color_id);
    // Get color value
    var color = $(el).children('div.color').css('background-color');
    console.log(color);
    // Set it to current color
    $('.current').css('background-color', color);
    $(el).siblings('li').addClass('active');
}
