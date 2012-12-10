var ticketing = ticketing || {};

ticketing.dashboard = {
    init: function () {
        var statusElem = $('#status-save-button ul.dropdown-menu>li');

        statusElem.click(function (ev) {
            ev.preventDefault();
            $('#id_status').attr('value', $(this).data('status-id'));
            $(this).parents('form').submit();
        });

        $('#id_message_template').change(function (ev) {
            if (!$(this).val()) {
                $("#id_message_text").val('');
            }
            $.ajax({
                url: '/api/v1/communicationeventtype/' + $(this).val() + '/',
                data: {
                    ticket_id: $(this).parents('form').data('ticket-id')
                },
                contentType: 'application/json',
                beforeSend: function (jqXHR, settings) {
                    jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
                },
                success: function (data, textStatus, jqXHR) {
                    var iframeDoc = $('#id_message_text').siblings('iframe').contents();
                    $('body', iframeDoc).html(data.email_body_html_template);
                }
            });
        });

        $('#create-user-form').submit(function (ev) {
            ev.preventDefault();
            var form = $(this);
            var formUrl = $(this).attr('action');
            $.ajax({
                url: formUrl,
                type: $(this).attr('method'),
                contentType: 'application/json',
                data: JSON.stringify({
                    'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]', $(this)).val(),
                    'first_name': $('input[name="first_name"]', this).val(),
                    'last_name': $('input[name="last_name"]', this).val(),
                    'email': $('input[name="email"]', this).val()
                }),
                dataType: 'json',
                processData: false,
                beforeSend: function (jqXHR, settings) {
                    jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]', form).val());
                },
                success: function (data) {
                    $('#requester-create-form-modal').modal('hide');
                    $('#id_requester').val(data.value);
                    $('#id_requester_helper').val(data.label);
                },
                error: function (data) {
                    $("#id_email").parents('.control-group').addClass('error');

                    var helpBlock = $('#id_email').siblings('.help-block');
                    if (helpBlock.length) {
                        helpBlock.html(
                            "<i class='icon-exclamation-sign'></i>" + data.responseText
                        );
                    } else {
                        $("#id_email").after(
                            "<span class='help-block'>" +
                            "<i class='icon-exclamation-sign'></i>" +
                            data.responseText +
                            "</span>"
                        );
                    }
                }
            });
        });

    },
    initAutoComplete: function () {
        $('.autocomplete-field').each(function (elem) {
            var searchInput = $('[type=text]', this);
            var idInput = $('[type=hidden]', this);
            var sourceUrl = $(this).data('source-url');

            searchInput.autocomplete({
                minLength: 0,
                source: function (request, response) {
                    $.getJSON(sourceUrl, {
                        q: request.term
                    }, function (data) {
                        response(data.objects);
                    });
                },
                select: function (event, ui) {
                    searchInput.val(ui.item.label);
                    idInput.val(ui.item.value);
                    return false;
                }
            }).focus(function () {
                $(this).autocomplete("search");
            });
        });
    }
};
