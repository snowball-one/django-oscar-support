var support = support || {};

support.dashboard = {
    init: function () {
    },

    initAutoComplete: function () {
        $('.autocomplete-field').select2({
            minimumInputLength: 3,
            query: function (options) {
                var apiUrl = $(this)[0].element.data('source-url');
                var results = [];

                $.ajax({
                    url: apiUrl,
                    dataType: 'json',
                    data:  {
                        filter: options.term,
                    },
                    success: function (data) {
                        $.each(data, function (key, obj) {
                            results.push({
                                id: obj.id,
                                text: obj.display_text,
                            });
                        });
                        options.callback({more: false, results: results});
                    }
                });
            },
            /**
             * Initialise the select2 element with the ID in the value. This
             * requests the corresponding entity (given bey the source URL with
             * the specified ID and passes the returned object to select2.
             * If no value is present, the lookup is ignored.
             *
             */
            initSelection: function (element, callback) {
                var elemValue = $(element).val();
                if (elemValue === null) {
                    return;
                }
                $.ajax({
                    url: $(element).data('source-url') + elemValue + '/',
                    dataType: 'json',
                    success: function (data) {
                        callback({id: data.id, text: data.display_text});
                    }
                });
            }
        });
    }
};
