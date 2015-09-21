+function ($) {
  'use strict';
    $(document).on('click', '.dropdown-menu ul>li', function(){
        var text = $(this).text();
        var value = $(this).attr('data-value');
        //console.log(text, value);
        var $dropdown = $(this).parents('.dropdown');
        $dropdown.find('[data-toggle=dropdown]').attr('data-value', value);
        $dropdown.find('.selected-text').text(text);
    })
}(jQuery);