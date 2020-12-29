function checkAccount(username){
		if (username == '') {
			$('.num-err').removeClass('hide').find("em").text('请输入账户');
			return false;
		} else {
			$('.num-err').addClass('hide');
			return true;
		}
	}

	function checkPass(pass){
		if (pass == '') {
			$('.pass-err').removeClass('hide').text('请输入密码');
			return false;
		} else {
			$('.pass-err').addClass('hide');
			return true;
		}
	}
function langBtn(){
				var name = $.trim($('#tel').val());
				var pass = $.trim($('#passport').val());
				var pass2 = $.trim($('#passport2').val());
				if (checkAccount(name) && checkPass(pass)&&checkPass(pass2)) {
				    if (pass==pass2){
				        var ldata = {username:name,password:pass};
                        $.ajax({
                            url: '/doreg/',
                            type: 'post',
                            dataType: 'json',
                            async: true,
                            data: ldata,
                            success:function(data){
                                if (data !=="") {
                                    window.location.href=data['data'];//需要跳转的地址
                                    console.log(data)
                                }
                            },
                            error:function(){
                            }
                        });
                    }
				} else {
					return false;
				}
	}