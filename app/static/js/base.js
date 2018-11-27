$(function () {
    var email = /^\w*@\w*\.\w*$/
    var flag1 = false
    $("#email").change(function () {
        $(this).parent().find("i").remove()
        console.log($(this).val())
        if (email.test($(this).val())) {
            console.log("true")
            data = {
                "email": $(this).val()
            }
            $.get("/checkemail/", data, function (response) {
                console.log(response)
                if (response['msg']) {
                    // console.log("可以注册")
                    $("#email").parent().removeClass("has-error").addClass("has-success")
                    flag1 = true

                } else {
                    $("#email").val("").attr("placeholder", "邮箱已注册")
                    $("#email").parent().addClass("has-error has-feedback").removeClass("has-success")
                    console.log("不可注册")
                    flag1 = false
                }
            })
        } else {
            $("#email").val("").attr("placeholder", "请填写正确的邮箱格式")
            $("#email").parent().addClass("has-error has-feedback").removeClass("has-success")
            console.log("false")
            flag1 = false
        }
    })


    function test(pattern, str, _this) {
        if (pattern.test(str)) {
            _this.parent().removeClass("has-error").addClass("has-success")
            return true
        } else {
            _this.parent().addClass("has-error has-feedback").removeClass("has-success")
            console.log("false")
            return false
        }
    }
    $("#passwd1").attr("placeholder","密码6-12位")
    var flag2 = false
    $("#passwd1").change(function () {
        console.log($(this).val())
        flag2 = test(/^\w{6,12}$/,$(this).val(),$(this))
        if (!flag2) {
            $(this).val("").attr("placeholder", "密码6-12位")
        }

    })
    var flag3 = false
    $("#passwd2").attr("placeholder","密码6-12位")
    $("#passwd2").change(function () {
        if (!flag2) {
            $(this).val("").attr("placeholder", "格式不对")
            $(this).parent().addClass("has-error has-feedback").removeClass("has-success")
            flag3 = false
        } else {
            if ($("#passwd1").val() != $("#passwd2").val()) {
                $(this).val("").attr("placeholder", "与第一次密码不同")
                $(this).parent().addClass("has-error has-feedback").removeClass("has-success")
                flag3 = false
            } else {
                $(this).parent().addClass("has-success").removeClass("has-error")
                flag3 = true
            }
        }
    })

    var count = 5
    $("#getcode").click(function () {
        count = 5
        _this = $(this)
        _this.attr("disabled","disabled")
        function countTime() {
            count--
            console.log(count)
            _this.val("重新发送("+count+")s")
            if(count==0){
                _this.removeAttr("disabled")
                _this.val("获取验证码")
            }
            if (count > 0) {
                setTimeout(countTime, 1000)
            }

            return false
        }
        countTime()

        data = {
            'email': $("#email").val()
        }
        $.get(/senderemail/, data, function (response) {
            console.log(response)
            $(".register").attr("code", response['code'])
        })
        console.log("click")
    })
    $(".register").click(function(){
        if(flag1&&flag2&&flag3){
            if($("#checkcode").val()!=$(this).attr("code")){
                $("#checkcode").val("")
                $("#checkcode").attr("placeholder","验证码错误")
                $("#checkcode").parent().addClass("has-error has-feedback").removeClass("has-success")
            return false
            }
            if(!$("#icon").val()){
                alert("请上传头像")
                return false
            }

        }
        else{
            alert("请仔细核对信息后重试")
        }
    })

    $(".login11").click(function(e){
        if(!$("#passwd11").val()||!$("#email11").val()){//邮箱或者账号为空
            alert("填写完整信息")
            e.preventDefault()
            return false
        }
        else{
            data = {
                'email':$("#email11").val(),
                "passwd":$("#passwd11").val()
            }
            _this = $(this)
            $.get("/login/",data,function(response){
                console.log(response)
                if(response['msg']=='1'){//输入正确
                    _this.attr("flag",'1')
                }
                else{//输入错误
                    _this.attr("flag",'0')
                    alert("账号或者密码错误")

                }
            })
            if(_this.attr("flag")=='0'){
                e.preventDefault()
                    return false
            }

        }
    })

    

})