(function($){
    $('.textarea-group.limitText').each(function(){
        var _this = this;
        var $textarea = $(_this).find('textarea');
        var maxNumber = $(_this).data('max-number');
        var extraNumber = maxNumber - $textarea.val().length;
        var info = "<span class='limit-info'>"+extraNumber+"/"+maxNumber+"</span>";
        $(_this).append(info);

        var fn = function() {
            var extraNumber = maxNumber -$textarea.val().length;
            if (extraNumber >= 0) {
                $(_this).find('.limit-info').html(extraNumber + '/' + maxNumber);
            }
            else {
                $(_this).find('.limit-info').html('<b style="color:red;">' + extraNumber + '</b>/' + maxNumber);
            }
        };

        //绑定输入事件监听器
        if(window.addEventListener) { //先执行W3C
            $textarea.get(0).addEventListener("input", fn, false);
        } else {
            $textarea.get(0).attachEvent("onpropertychange", fn);
        }
        if(window.VBArray && window.addEventListener) { //IE9
            $textarea.get(0).attachEvent("onkeydown", function() {
                var key = window.event.keyCode;
                (key == 8 || key == 46) && fn();//处理回退与删除
            });
            $textarea.get(0).attachEvent("oncut", fn);//处理粘贴
        }
    });
})(jQuery);