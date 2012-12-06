var ticketing = ticketing || {};

ticketing.dashboard = {
    init: function () {
        var statusElem = $('#status-save-button ul.dropdown-menu>li');

        statusElem.click(function (ev) {
            ev.preventDefault();
            $('#id_status').attr('value', $(this).data('status-id'));
            $(this).parents('form').submit();
        });
    }
};
