/**
 * Created with PyCharm.
 * User: geaden
 * Date: 9/26/13
 * Time: 6:57 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function() {
    datePicker();
})



/**
 * Datepicker settings
 */
function datePicker() {
    $('.datepicker').datepicker({
        dateFormat: "dd.mm.yy",
        showButtonPanel: true,
        showWeek: true,
        changeYear: true
    });
}