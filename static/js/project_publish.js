+function ($) {
    'use strict';

    //region COMMON
    //save step to localstorage, next time can start from the break point.
    var currentStep = function(){
        if(window.localStorage){
            var currentStep = window.localStorage.currentStep;
            if(!currentStep){
                currentStep = 1;
                window.localStorage.currentStep = currentStep;
            }
            $('.step-content').each(function(){
                $(this).toggleClass('hide', true);
            });
            $('#publish_step_'+currentStep).toggleClass('hide', false);
            $('#steps_nav').attr('data-current-step', currentStep);
            $('.steps-nav-item').each(function(index){
                if(index < currentStep){
                    $(this).addClass('finished');
                } else {
                    $(this).toggleClass('finished', false);
                }
            });
        }else{
            console.log('This browser does NOT support localStorage');
        }
    };
    currentStep();

    //change step
    var stepsOp = {
        data:{}
    };
    //before next step or prev step.
    var beforeForward = function(nextStep,callback){
        var currentStep = $('#steps_nav').data('current-step');
        if(nextStep < currentStep){
            callback();
            return;
        }
        if(!stepsOp["validate"+currentStep]()){
            return false;
        }
        stepsOp["save"+currentStep](callback);
    };
    //next step or prev step.
    $(document).on('click', '.step-forword-button', function(){
        var _this = this;
        var nextStep = $(_this).data('step-forward');
        beforeForward(nextStep, function(){
            $(_this).parents('.step-content').toggleClass('hide', true);
            $('#publish_step_' + nextStep).toggleClass('hide',false);
            $('.steps-nav-item').each(function(index){
                if(index < nextStep){
                    $(this).addClass('finished');
                } else {
                    $(this).toggleClass('finished', false);
                }
            });
            $('#steps_nav').data('current-step', nextStep);
            window.localStorage.currentStep = nextStep;
        });
    });
    //endregion



    //region =====STEP1
    var editor = new Simditor({
        textarea: $('#project-description'),
        upload:{

            url: '/simeditor_upload',
            params: null,
            fileKey: 'upload_file',
            connectionCount: 3,
            leaveConfirm: 'Uploading is in progress, are you sure to leave this page?'
        }
        //optional options
    });

    //categories selecte
    $(document).on('click', 'ul#publish-categories>li', function(){
        $('ul#publish-categories>li').toggleClass('active', false);
        $(this).addClass('active');
    });
    //display title in preview on the right hand when change the title
    $(document).on('change', '#project-name', function(){
       var name = $(this).val();
        $('#publish_step_1').find('.project .title').text(name);
    });
    //set city when selected province.
    $(document).on('change','#province', function(){
        var $city = $('#city');
        $city.html('<option value="-1">请选择</option>');
        var province = $(this).val();
        if(province == -1){
            return;
        }
        var data = {province: province};
        $.ajax({
            type: 'GET',
            url: '/comm/city',
            data: data,
            dataType: 'json',
            success:function(res){
                console.log(res);
                if(res.code == 0){
                    for(var i = 0; i < res.cities.length; i++){
                        for(var key in res.cities[i]){
                            var html = '<option value="'+key+'">'+res.cities[i][key]+'</option>';
                            $city.append(html);
                        }
                    }
                }
            }
        })
    });

    //select video to upload
    // $(document).on('change','#project-video input[type=file]', function(){
    //     var filename= $(this).val();
    //     var $currentFile = $('#project-video .current-file');
    //     $currentFile.find('.file-name').text(filename);
    //     $currentFile.toggleClass('hide',false);
    //     $('#project-video input[type=submit]').toggleClass('hide',false);
    //     $('#project-video .input-file').toggleClass('hide', true);
    // });
    //delete selected video
    // $(document).on('click', '#project-video .delete-file', function(){
    //     var $projectVideo = $('#project-video');
    //     $projectVideo.find('input[type=file]').val('');
    //     $projectVideo.find('.current-file .file-name').text('');
    //     $projectVideo.find('.current-file').toggleClass('hide',true);
    //     $projectVideo.find('input[type=submit]').toggleClass('hide',true);
    //     $projectVideo.find('.input-file').toggleClass('hide', false);
    // });

    //select picture to upload
    var html5Reader = function(file, preview){
        var file = file.files[0];
		var reader = new FileReader();
		reader.readAsDataURL(file);
		reader.onload = function(e){
			preview.src=this.result;
		}
    }
    var generateImagePreview = function(file, preview){
        if (document.all) {
            file.select();
            var reallocalpath = document.selection.createRange().text;
			var ie6 = /msie 6/i.test(navigator.userAgent);
			// IE6浏览器设置img的src为本地路径可以直接显示图片
            if (ie6) {
                preview.src = reallocalpath;
            }
            else {
				// 非IE6版本的IE由于安全问题直接设置img的src无法显示本地图片，但是可以通过滤镜来实现
                preview.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod='image',src=\"" + reallocalpath + "\")";
				// 设置img的src为base64编码的透明图片 取消显示浏览器默认图片
                preview.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==';
            }
        }else{
    		html5Reader(file, preview);
		}
    };
    $(document).on('change', '#project-cover input[type=file]', function(){
        var file = this;
        var preview = $('.cover-preview').get(0);
		var ext=file.value.substring(file.value.lastIndexOf(".")+1).toLowerCase();
		// gif在IE浏览器暂时无法显示
		if(ext!='png'&&ext!='jpg'&&ext!='jpeg'){
			alert("文件必须为图片！");
            return;
		}
        generateImagePreview(file, preview);

        $('#project-cover input[type=button]').toggleClass('hide',false);
    });

    //点击上传按钮触发长传事件

    $(document).on('click','#project-cover input[type=button]',function(){
        $('#project_cover_form').ajaxSubmit({success:function(data){

            if(data.success){
                $('#project_cover_file').attr('data-file-url',data.file_path);
                alert("文件上传成功");

            }else{
                alert("文件上传失败");
            }
            console.log(data);
        }});


    });

    stepsOp.validate1 = function(){
        //category
        stepsOp.data = {};
        // var category = $('#publish-categories>li.active');
        // if(!category || category.length == 0){
        //     alert("请选择类别!");
        //     comm.goToElement($('#publish-categories'));
        //     return false;
        // }
       // stepsOp.data["category"] = category;
        //title
        var title = $('#project-name').val();
        if(!title || title.length > 25){
            alert("项目名称不能为空, 并且长度不能大于25!");
            comm.goToElement($('#project-name'));
            return false;
        }
        stepsOp.data["title"] = title;
        //pic
        /* todo, because of not implement the upload backend,
           there's no url, so do this after implement the backend.*/
        //city
        // var city = $('#city').val();
        // if(!city || city == -1){
        //     alert("请选择发起城市!");
        //     comm.goToElement($('#city'));
        //     return false;
        // }
        // stepsOp.data["city"] = city;

        //video
        /*todo, video is as the same as the picture.*/

        //abstract
        var abstract = $('#project-abstract').val();
        if(!abstract || abstract.length > 50){
            alert("请填写项目概述, 并且长度不超过50字!");
            comm.goToElement($('#project-abstract'));
            return false;
        }
        stepsOp.data["abstract"] = abstract;
        //description
        var description = editor.getValue();
        if(!description){
            alert("请填写项目概述描述");
            comm.goToElement($('.simditor'));
            return false;
        }
        stepsOp.data["description"] = description;
        //days
        var days = $('#project-days').val();
        if(!days || days < 10 || days > 90){
            alert("请填写筹款天数, 其范围为10-90!");
            comm.goToElement($('#project-days'));
            return false;
        }
        stepsOp.data["days"] = days;
        //amt
        var amt = $('#project-amt').val();
        if(!amt || amt < 1000 || amt > 1000000000){
            alert("请填写筹款金额, 其范围为1000-1000000000!");
            comm.goToElement($('#project-amt'));
            return false;
        }
        stepsOp.data["amt"] = amt;
        //prepay
        var prepay = $('#project-prepay').val();
         if(!prepay || prepay < 1 || prepay > 100){
            alert("请填写筹款金额, 其范围为1-100!");
            comm.goToElement($('#project-prepay'));
            return false;
        }
        stepsOp.data["prepay"] = prepay;

        var policy = $('#step_1_policy').prop('checked');
        if(!policy){
            alert("您必须要同意平台服务协议，才能继续!");
            comm.goToElement($('#step_1_policy'));
            return false;
        }
        return true;
    };
    stepsOp.save1 = function(callback){
        //todo, ajax commit.
        callback();
    };
    //endregion

    //region =====STEP2
    //add payback, pop up a modal to fill infos.
    var $addPayBackModal =  $('#add_payback_modal');
    var clearForm = function($form){
        $form.find('input[type=text]').val("");
        $form.find('input[type=file]').val("");
        $form.find('input[type=radio]').prop("checked", false);
        $form.find('textarea').val("");
    };
    $(document).on('click', '#add_payback', function(){
        clearForm( $('#add_payback_modal'));
        $('#add_payback_modal').modal('show');
    });
    $(document).on('change', '#payback_amt', function(){
        var amt = $(this).val();
        $addPayBackModal.find('.pay-back .amt>span').text(amt);
    });
    $(document).on('change', '#payback_title', function(){
        var title = $(this).val();
        $addPayBackModal.find('.pay-back .title').text(title);
    });
    $(document).on('change', '#payback_desc', function () {
        var desc = $(this).val();
        $addPayBackModal.find('.pay-back .description').text(desc);
    });
    $(document).on('change', 'input[name=shippingType]', function(){
        var shipping = $('input[name=shippingType]:checked').parent().text();
        $addPayBackModal.find('.pay-back .transport').text(shipping);
    });
    $(document).on('change', '#send_time', function(){
        var sendTime = $(this).val();
        $addPayBackModal.find('.pay-back .payback-time>span').text(sendTime);
    });
    $(document).on('change', '#pay_back_image input[type=file]', function(){
        var file = this;
        var preview = $addPayBackModal.find('.pay-back .image-preview > img').get(0);
		var ext=file.value.substring(file.value.lastIndexOf(".")+1).toLowerCase();
		// gif在IE浏览器暂时无法显示
		if(ext!='png'&&ext!='jpg'&&ext!='jpeg'){
			alert("文件必须为图片！");
            return;
		}
        generateImagePreview(file, preview);
    });

    var validatePayBack = function($form){
        stepsOp.data ={};

        var amt = $form.find('#payback_amt').val();
        if(!amt || amt <= 0){
            alert("请正确填写回报金额, 需为大于0的数字");
            comm.goToElement($form.find('#payback_amt'));
            return false;
        }
        stepsOp.data["amt"] = amt;

        var title = $form.find('#payback_title').val();
        if(!title || title.length > 25){
            alert("请填写标题，长度不得大于25");
            comm.goToElement($form.find('#payback_title'));
            return false;
        }
        stepsOp.data["title"] = title;

        var desc = $form.find('#payback_desc').val();
        if(!desc || desc.length > 100){
            alert("请填写描述，长度不得大于100");
            comm.goToElement($form.find('#payback_desc'));
            return false;
        }
        stepsOp.data["desc"] = desc;

        var paybackNumber = $form.find('input[name=paybackNumber]:checked').val();
        if(!paybackNumber){
             alert("请选择回报数量！");
            comm.goToElement($form.find('input[name=paybackNumber]'));
            return false;
        }
        stepsOp.data["paybackNumber"] = paybackNumber;

        var personLimit = $form.find('input[name=personLimit]:checked').val();
        if(!personLimit){
            alert("请选择个人限够！");
            comm.goToElement($form.find('input[name=personLimit]'));
            return false;
        }
        stepsOp.data["personLimit"] = personLimit;

        //todo, image.

        var shipping = $form.find('input[name=shippingType]:checked').val();
        if(!shipping){
            alert("请选择物流方式！");
            comm.goToElement($form.find('input[name=shippingType]'));
            return false;
        }
        stepsOp.data["shipping"] = shipping;

        var sendTime = $form.find('#send_time').val();
        if(!sendTime || sendTime <= 0){
            alert("请正确填写发放时间！");
            comm.goToElement($form.find('#send_time'));
            return false;
        }
        stepsOp.data["sendTime"] = sendTime;
        return true;
    };
    var savePayBack = function(){
        $.ajax({
            type:'POST',
            data: stepsOp.data,
            url:'/project/payback',
            dataType: 'html',
            success: function(res){
                //console.log(res);
                $('#paybacks').append(res);
                $('#add_payback_modal').modal('hide');
            }
        })
    };
    stepsOp.validate2 = function(){
        var paybackNumber = $('#paybacks .pay-back').length;
        if(paybackNumber == 0){
            alert("请至少增加1个回报!")
            return false;
        }
        return true;
    };
    stepsOp.save2 = function(callback){callback()};
    $(document).on('click', '#submit-payback', function(){
        if(validatePayBack($('#payback_info'))){
            savePayBack();
        }
    });

    //endregion
}(jQuery);