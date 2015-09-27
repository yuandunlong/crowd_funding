var comm = function($){
    var common = {};
    common.goToElement = function($obj) {
	    var _targetTop = $obj.offset().top;//获取位置
	    jQuery("html,body").animate({scrollTop:_targetTop},300);//跳转
    };
    return common;
}(jQuery);