$(function () {
    if (!$('#googlepaypassesmodal .modal-dialog').length) {
        return;
    }

    $('#googlepaypassesmodal .modal-dialog').each(function () {
        // .modal-backdrop has a z-index of 1040
        // .modal has a z-index of 1050
        // Yet, this modal is shown underneath the backdrop. Not sure, if this bug
        // is pretix, bootstrap or - more probably - plugin related.
        $(this).css('z-index', 1060);
    });

    let imgPath = $('#buttonScript').attr("imgPath");

    $('form[action*="wallet"]>button').each(function (idx) {
        if ($(this).hasClass("btn-lg")) {
            // Large button
            $(this).html(`<img src="${imgPath}"/>`)
            $(this).removeClass("btn-default")
            $(this).addClass("btn-link")
        }
        if ($(this).hasClass("btn-sm")) {
            // Small button
            $(this).html(`<img src="${imgPath}" width="150px"/>`)
            $(this).removeClass("btn-default")
            $(this).addClass("btn-link")
        }
    })


    $('form[action*="wallet"]').click(function (event) {
        event.preventDefault();
        $('#googlepaypassesmodal form').attr('action', $(this).attr('action'));
        $('#googlepaypassesmodal form input[name=csrfmiddlewaretoken]').attr('value', $('input[name=csrfmiddlewaretoken]:last').val());
        $('#googlepaypassesmodal').modal('toggle');
        return false;
    });
});