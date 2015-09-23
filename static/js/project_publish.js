+function ($) {
    'use strict';
    var editor = new Simditor({
        textarea: $('#project-description')
        //optional options
    });

    //add payback, pop up a modal to fill infos.
    $(document).on('click', '#add_payback', function(){
        $('#add_payback_modal').modal('show');
    });
}(jQuery);