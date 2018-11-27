$(function(){
    $(".to_cart").click(function(){
        data = {
            "goodsid":$(this).attr("goodsid")
        }
        $.get("/addtocart/",data,function (response) {
            console.log(response)
            if(response["msg"]){
                alert("已经添加到购物车")
                console.log("添加成功")
            }
            else{
                $("#login").trigger("click")
            }
        })
    })
})