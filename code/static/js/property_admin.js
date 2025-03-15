(function($) {
    $(document).ready(function() {
        function toggleFields() {
            var projectSelected = $('#id_project').val(); 
            var rateType = $('#id_rate_type').val();

            if (projectSelected) {
                $('.field-rate_type').closest('.form-row').hide();
                $('.field-size').closest('.form-row').hide();
                $('.field-price').closest('.form-row').hide();
                $('.field-rate').closest('.form-row').hide();
            } else {
                $('.field-rate_type').closest('.form-row').show();
                $('.field-size').closest('.form-row').show();
                $('.field-price').closest('.form-row').show();
                $('.field-rate').closest('.form-row').show();
                
                if (rateType === 'direct') {
                    $('#id_size').parent().hide();
                } else if (rateType === 'sqfeet') {
                    $('#id_size').parent().show();
                }
                $('#id_price').parent().show();
            }
        }
        toggleFields();
        $('#id_project').change(function() {
            toggleFields();
        });
        $('#id_rate_type').change(function() {
            toggleFields();
        });
    });
})(django.jQuery);
