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
    },
    initAutoComplete: function () {
        console.log('autocomplete intialising');
        $('.autocomplete-field').each(function (elem) {
            var searchInput = $('[type=text]', this);
            var idInput = $('[type=hidden]', this);
            var sourceUrl = $(this).data('source-url');

            console.log('using source url', sourceUrl);

            searchInput.autocomplete({
                minLength: 2,
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
            });
        });
    }
};
