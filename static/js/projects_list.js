+function ($) {
  'use strict';
    //=== 选中category
    $(document).on('click', '.category', function(){
        $('.category.selected').removeClass('selected');
        $(this).addClass('selected');
        //TODO, 提交请求重新请求数据
    })
}(jQuery);