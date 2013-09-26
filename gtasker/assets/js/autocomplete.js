
var shownSuggestions = false;
var followerSelected = true;


$(document).ready(function() {
    removeFollower();
    hideSuggestions();
    $('li .item').hover(function() {
        console.log('follower!');
        followerSelected = true;
    }, function() {
        followerSelected = false;
    })
});


/**
 * Autocomplete using jquery;
 */
function followersAutocomplete() {
     var noQ = [
         '<li><a href="#" class="disabled">',
            '<span class="glyphicon glyphicon-search"></span>&nbsp;',
            '<strong>Start typing...</strong></a>',
        '</li>'];
     var template = [
            '<div class="dropdown open col-lg-10">',
            '<ul class="dropdown-menu autocomplete">',
            noQ.join(''),
            '</ul>', '</div>'];
    $("#id_followers_autocomplete").focus(function() {
        // Check whether suggestions are shown
        console.log('focusing...' + shownSuggestions);
        $(this).siblings('.dropdown').remove();
        if (!shownSuggestions) {
            $(this).after(template.join(''));
            shownSuggestions = true;
        }
    });
    $("#id_followers_autocomplete").on('input', function(el) {
        var q = $(el.target).val();
        var loader = ['<li><a href="#" class="text-center">',
            '<img src="/static/img/ajax-loader.gif" />',
            '</a></li>'];
        $('ul.dropdown-menu.autocomplete').html(loader.join(''));
        $.ajax({
            url: "/profiles/autocomplete/?q=" + q,
            method: "GET",
            success: function (data) {
                var followers = [];
                if (data.length) {
                    for (var i = 0; i < data.length; i++) {
                        var value = data[i];
                        console.log(value);
                        var follower = value.fields;
                        console.log(follower);
                        var picture = (follower.picture) ?
                            follower.picture : "https://lh4.googleusercontent.com/-2jhswoDd3mQ/AAAAAAAAAAI/AAAAAAAAAEQ/HijQ3Vzn0Hw/photo.jpg"
                        followers.push('<li><a href="#" data-value="' + value.pk + '" onclick="selectFollower(this)">'
                            + '<div class="item">'
                                    + '<img class="item img-thumbnail" src="' + picture + '" />'
                                    + '<dl><dt>' + follower.first_name
                                    + ' ' + follower.last_name + '</dt>'
                                    + '<dd><small>' + follower.email + '</small></dd></dl>'
                            + '</div>'
                            + '</a></li>');
                    }
                    $('ul.dropdown-menu.autocomplete').empty();
                    $('ul.dropdown-menu.autocomplete').html(followers.join(''))
                    console.log(data);
                } else {
                    var noData = ['<li class="">',
                        '<a href="#" class="disabled">',
                        '<strong>No followers found :(</strong>',
                        '</a>',
                        '</li>'];
                    $('ul.dropdown-menu.autocomplete').empty();
                    if (q) {
                        $('ul.dropdown-menu.autocomplete').html(noData.join(''));
                    } else {
                        $('ul.dropdown-menu.autocomplete').html(noQ.join(''));
                    }
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
}

/**
 * Select follower
 * @param element
 */
function selectFollower(el) {
    console.debug('Selecting...');
    $(el).parents('.dropdown').removeClass('open');
    shownSuggestions = false;
    var value = $(el).data('value');
    console.log($(el).children('img.itme'));
    if (!$('#id_followers_' + value).length) {
        $('#id_followers_autocomplete').after('<div class="panel panel-default follower">'
            + '<div class="panel-body follower">'
            + '<button type="button" data-toogle="tooltip" title="Remove follower" class="close" data-dismiss="follower" data-value="'
            + value + '">×</button>'
            + '<div class="clearfix follower">' + $(el).children('.item').html() + '</div></div></div>');
        $('#id_followers_autocomplete').before('<input type="hidden"'
            + ' id="id_followers_' + value + '" name="followers" value="' + value + '" />'
        );
    }
    $('#id_followers_autocomplete').val('');
}


/**
 * Remove followers
 */
function removeFollower() {
    $(document).on('click', 'button[data-dismiss=follower]', function(e) {
        console.debug('Removing by clicking at' + $(e.target).html());
        var follower = $(e.target).data('value');
        $('#id_followers_' + follower).remove();
        $(e.target).parents('.panel').remove();
    });
}

/**
 * Hide autocomplete dropdown
 */
function hideSuggestions() {
    $('#id_followers_autocomplete').unbind().blur(function(e) {
        if (shownSuggestions && !followerSelected) {
            console.log('hiding...');
            $(this).siblings('.dropdown').removeClass('open');
            shownSuggestions = false;
        }
    });
}


