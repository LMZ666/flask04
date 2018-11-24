$(function () {
    var email = /^\w*@\w*\.\w*$/
    $("#email").change(function () {
        console.log($(this).val())
        if (email.test($(this).val())){
            console.log("true")
        }
        else{
            console.log("false")
        }
        var i = $("<i style='color: red'>邮箱格式不对</i>")
        $(this).parent().append(i)
    })

    $("#passwd1").change(function () {
        console.log($(this).val())
    })

    $("#passwd2").change(function () {
        console.log($(this).val())
    })

    $("#checkcode").click(function () {
        console.log($(this).val())
    })

    $("#getcode").click(function () {
        console.log("click")
    })

})