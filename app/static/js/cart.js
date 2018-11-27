$(function(){
    $("#cart").addClass("active")
    function sumprice(){
        var sum = 0
        $(".media-body").each(function(){
        var price = $(this).find("i").html().substring(1)
        var num = $(this).find("p").html()
        sum+=parseFloat(price)*parseInt(num)
    })
        $("#sum").html("总价："+sum).css({"color":"red"})
    }
    sumprice()
    $(".minus").click(function(){
        var num = parseInt($(this).next().html())
        console.log($(this).next())
        console.log(num)
        num -= 1
        $(this).next().html(num)
        if(num==0){
            $(this).parent().parent().parent().remove()
        }
        data={
            "goodid":$(this).parent().attr('goodid')
        }
        $.get("/minus/",data,function(response){
            console.log(response)
        })
        sumprice()
    })
    $(".add").click(function(){
        var num = parseInt($(this).prev().html())
        num+=1
        $(this).prev().html(num)
        data={
            "goodid":$(this).parent().attr('goodid')
        }
        $.get("/add/",data,function (response) {
            console.log(response)
        })
        sumprice()
    })
    $("#pay").click(function(){
        
    })
})