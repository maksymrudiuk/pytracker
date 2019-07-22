function fadeInMessage(){
    $('.message').fadeOut(1500);
}

function addDeveloperInProject() {
    var indicator = $("#ajax-progress-indicator");
    var errorindicator = $("#ajax-error");

    $('.add-btn').click(function(event){
        var box = $(this);
        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': false,
            'dataType': 'json',
            'data': {
                'pk': box.data('developer-id'),
                'slug': box.data('project-slug'),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function(xhr, settings){
                indicator.show();
            },
            'error': function(xhr, status, error){
                errorindicator.show();
                indicator.hide(1500);
            },
            'success': function(data, status, xhr){
                indicator.hide(1500);
                location.reload();
            }
        });
    });
}

function digital_clock() {
    setInterval( function() {
        var date = new Date();
        hours = date.getHours();
        $(".hours").html(( hours < 10 ? "0" : "" ) + hours);
        }, 100);
    setInterval( function() {
        var minutes = new Date().getMinutes();
        $(".minutes").html(( minutes < 10 ? "0" : "" ) + minutes);
        },100);
    setInterval( function() {
        var seconds = new Date().getSeconds();
        $(".seconds").html(( seconds < 10 ? "0" : "" ) + seconds);
        },100);
}

function deleteDeveloperFromProject() {
    var indicator = $("#ajax-progress-indicator");
    var errorindicator = $("#ajax-error");

    $('.delete-developer-btn').click(function(event){
        var box = $(this);
        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': false,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function(xhr, settings){
                indicator.show();
            },
            'error': function(xhr, status, error){
                console.log('DELETE ERROR')
                errorindicator.show();
                indicator.hide(1500);
            },
            'success': function(data, status, xhr){
                indicator.hide(1500);
                location.reload();
            }
        });
    });
}

function getTask() {

    var errorMessage = $('#ajax-error');

    $('.set-dev-task-btn').click(function(event){
        var obj = $(this);
        $.ajax(obj.data('url'), {
            'type': 'POST',
            'async': false,
            'dataType': 'json',
            'data': {
                'pk': obj.data('developer-id'),
                'task_id': obj.data('task-id'),
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'error': function(xhr, status, error) {
                errorMessage.show()
            },
            'success': function(data, status, xhr) {
                location.reload();
            }
        })
    })
}

$(document).ready(function(){
    fadeInMessage(); // Hide status message
    addDeveloperInProject(); // Ajax add developer in project
    deleteDeveloperFromProject(); // Ajax delete performer from Project
    getTask(); // Get Task for deveper and set developer in task for admin
    digital_clock(); // digital clock script set time values in html
});

