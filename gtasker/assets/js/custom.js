/**
 * Custom JS methods in order to enhance interation
 */
$(document).ready(function() {
    // Prepare tooltips
    $("#add_project").tooltip();
    // Prepare modals
    $("#add_project").click(function() {
        $("#project_modal").modal('show');
        followersAutocomplete();
    });
    createTask();
    saveProject();
    projectDetails();
})

/**
 * Clears inputs for provided form
 * @param form
 */
function clearInputs(form) {
    $('.alert').alert('close');
    $(':input', form)
        .not(':button, :submit, :reset, :hidden')
        .val('')
        .removeAttr('checked')
        .removeAttr('selected');
}

/**
 * Shows project details window
 */
function projectDetails() {
    $(document).on('click', '.project_detail_link', function(e) {
        clearActiveProjects();
        $(e.target).parents('tr').addClass("success")
        $('#projects_list').removeClass('col-lg-10').
            addClass('col-lg-6');
        $('#project_details').show();
        $('#project_details').animate({
            marginLeft: parseInt($(this).css('margin-lef'), 10) == 0 ?
                $(this).outerWidth() : 0
        });
        editProject();
    })
}

/**
 * Clear active project
 */
function clearActiveProjects() {
    $('tr.success').removeClass('success');
}


/**
 * Closes project details
 */
function closeProjectDetails() {
    clearActiveProjects();
    $('#project_details').hide();
    $('#projects_list').removeClass('col-lg-6').
            addClass('col-lg-10');
}


/**
 * Edit project
 */
function editProject() {
    var project_name;
    var panelShown;
    // Mouse over
    $(document).on('hover', '#modal_project_name', function(e) {
        if (!panelShown) {
            $(e.target).after('<span class="glyphicon glyphicon-edit"></span>');
            panelShown = true;
        }
    }, function(e) {
         $(e.target).find("span:last").remove();
    });

    // Clicking
    $(document).on('click', '#modal_project_name', function(e) {
        project_name = $(e.target).text();
        console.log(project_name);
        $(e.target).replaceWith(
            ['<div class="form-group col-lg-offset-2">',
             '<input id="project_edit_name" type="text" class="form-control" value="' +
                project_name + '" name="name" />',
             '</div>'].join('')
            );
        $('#project_edit_name').focus();
    });

    // Focusing out
    $(document).on('focusout', '#project_edit_name', function(e) {
        console.log('focused out...');
        $(e.target).parent().replaceWith(
            [
                '<h1 id="#modal_project_name">',
                project_name,
                '</h1>'
            ].join('')
        );
        editProject();
    })
}


/**
 * Load project details
 */
function loadProjectDetails(el) {
    var project = $(el).data('value');
    // Empty tasks list for provided project
    $('#tasks_list').html('<img src="/static/img/ajax-loader.gif" />');
    $.ajax({
        async: true,
        url: '/' + project + '?ajax',
        method: 'GET',
        success: function(data) {
            console.debug(data);
            var output = ['<h1 id="modal_project_name">', data.name,
                '</h1>',
                '<h5 id="modal_project_notes">',
                data.notes,
                '</h5>']
            $('.project_details_header').html(output.join(''));
            var tasks = [];
            for (var i = 0; i < data.tasks.length; i++) {
                var task = data.tasks[i];
                console.log(task);
                tasks.push('<li><input type="checkbox" data-value="' +
                    data.pk + '"/>&nbsp;' + task.name + '</li>');
            }
            $('#tasks_list').html('');
            $('#tasks_list').append(tasks.join(''));
            $('#task_form #id_project').val(project);
            $('#task_form').show();
        },
        error: function(error) {
            $('.project_details_modal_body').html([
                '<h1>Error loading project info :(</h1>'].join(''));
        }
    })
}


/**
 * Create task
 */
function createTask() {
    var hasErrors = {};
    var form = $('#task_form');
    form.submit(function(e) {
        e.preventDefault();
        var url = $(form).attr('action');
        var formData = form.serializeArray();
        console.log(formData);
        $.ajax({
            url: url + '?ajax',
            method: 'post',
            data: formData,
            statusCode: {
                400: function (error) {
                    ajaxFormHandler('#task_form', error, {error: true}, hasErrors);
                },
                200: function(data) {
                    console.log(data);
                    ajaxFormHandler('#task_form', data, {}, hasErrors);
                    $('#tasks_list').append('<li><input type="checkbox" class="mark_done" data-value="' +
                        data.pk + '"/>&nbsp;' + data.name + '</li>');
                    $('#task_form #id_name').val('');
                }
            }
        });
    });
}


/**
 * Ajax form handler
 */
function ajaxFormHandler(formSelector, data, options, hasErrors) {
    var form = $(formSelector);
    if (options.error) {
        // Mark as error field
        var errors = $.parseJSON(data.responseText);
        console.log(errors);
        for (var field in errors) {
            console.log(hasErrors);
            if (!hasErrors["#id_" + field]) {
                $(form.find("#id_" + field).get(0)).parent().addClass('has-error');
                $(form.find("#id_" + field).get(0)).after(
                    errors[field].map(function(val) {
                        return '<span class="help-block">' + val + '</span>';
                    }).join()
                );
                hasErrors["#id_" + field] = true;
            }
            if (field === '__all__') {
                if (!hasErrors['#id____all__']) {
                    $('.alert').append(errors[field]);
                    $('.alert').addClass('alert-danger');
                    $('.alert').show();
                    hasErrors['#id____all__'] = true;
                }
            }
        }
        // Get rid of error class on field change
        form.find("input, textarea, select").one("keypress change", function(){
            $(this).parent().removeClass('has-error');
            console.log($(this).siblings("help-block"));
            $(this).siblings(".help-block").first().remove();
            hasErrors[$(this).attr('id')] = false;
        });
        console.log(hasErrors);
    } else {
         clearInputs(form);
         if (options.hide && options.modal) {
             $(options.modal).modal('hide');
         }
    }
}


/**
 * Parses date string and return in format 'dd.mm.yyyy'
 * @param dateString
 */
function parseDate(dateString) {
    var date = new Date(dateString);
    var yyyy = date.getFullYear().toString();
    var mm = (date.getMonth() + 1).toString(); // getMonth() is zero-based
    var dd  = date.getDate().toString();
    return (dd[1]?dd:"0"+dd[0]) + '.' + (mm[1]?mm:"0"+mm[0]) + '.' + yyyy;
}


/**
 * Saves project
 */
function saveProject() {
    var hasErrors = {};
    var form = $('#project_form');
    var url = form.attr('action');
    $('#save_project').click(function(e) {
        e.preventDefault();
        $.ajax({
            url: url + '?ajax',
            method: 'post',
            data: form.serializeArray(),
            statusCode: {
                400: function(error) {
                    ajaxFormHandler('#project_form', error, {error: true}, hasErrors);
                },
                200: function(data) {
                    ajaxFormHandler('#project_form', data, {modal: '#project_modal', hide: true}, hasErrors);
                    console.log(data);
                    var date_ranges;
                    if (data.start_date === null && data.finish_date === null) {
                        date_ranges = 'No date ranges';
                    } else if (data.finish_date == null) {
                        date_ranges = parseDate(data.start_date) + ' &ndash; Present';
                    } else {
                        date_ranges = parseDate(data.start_date) + ' &ndash; ' + parseDate(data.finish_date);
                    };
                    if ($('td.danger')) {
                        $('td.danger').remove();
                    }
                    $('#projects_list_table tbody').prepend(
                        ['<tr>',
                            '<td style="background-color: ' + data.color + ';"></td>',
                            '<td><a href="#project_details_modal" class="project_detail_link" onclick="loadProjectDetails(this)"'
                            + 'data-value="' + data.pk + '">' + data.name + '</a></td>',
                            '<td>' + data.notes + '</td>',
                            '<td>' + date_ranges + '</td>',
                        '</tr>'].join('')
                    );
                    $('.project_detail_link').on('click', function(e) {
                        loadProjectDetails(e.target);
                    })
                }
            }
        })
    })
}
