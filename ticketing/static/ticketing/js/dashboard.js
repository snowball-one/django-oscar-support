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
    }
};
