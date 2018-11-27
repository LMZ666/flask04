import random
import uuid

from flask import Blueprint, render_template, url_for, session, request, redirect, g, jsonify
from flask_mail import Message

from app.ext import db, cache, mail
from app.models import User, Goods, UserGoods

blue = Blueprint("bp",__name__)
def init_blue(app):
    app.register_blueprint(blueprint=blue)

@blue.route("/")
def index():
    # print(url_for("bp.addUser"))
    # 返回的是一个列表没有first()这个方法
    goods = Goods.query.all()[0]
    #
    wheels = [
        {"img":"img/wheel/wheel1.jpg"},
        {"img": "img/wheel/wheel2.jpg"},
        {"img": "img/wheel/wheel3.jpg"},
        {"img": "img/wheel/wheel4.jpg"},
        {"img": "img/wheel/wheel5.jpg"}
    ]
    classfiy = [
        {},
        {"name":"男装/毛衣/大衣"},
        {"name": "女装/内衣/毛衣"},
        {"name": "美妆/口红/遮瑕"},
        {"name": "女装/男装/内衣"},
        {"name": "女装/男装/内衣"},
        {"name": "女装/男装/内衣"},
        {"name": "女装/男装/内衣"},
    ]
    goods =Goods.query.all()
    count = 0
    # img / goods / 0.jpg
    for good in goods:
        good.img = "img/goods/"+str(count)+".jpg"
        count+=1
        db.session.add(good)
        db.session.commit()
    if g.user:
        return render_template("index.html",name = g.user.name,wheels= wheels,classfiy=classfiy,img=g.user.img,email = g.user.email)
    return render_template("index.html",wheels= wheels,classfiy=classfiy)

@blue.route("/shopping/")
def shopping():
    return render_template("shopping.html")

@blue.route("/cart/")
def cart():
    if g.user:
        carts = UserGoods.query.filter(UserGoods.u_user==g.user.id)
        if carts:
            goods=[]
            for cart in carts:
                good = Goods.query.get(cart.u_goods)
                goods.append((good,cart.num))
            return render_template('cart.html',  name=g.user.name, img=g.user.img, goods=goods)
    return render_template('cart.html')

@blue.route("/order/")
def order():
    return render_template("order.html")


@blue.route("/market/")
def market():
    page = int(request.args.get("page") or 1)
    per = 18
    paginates = Goods.query.paginate(page,per)
    if g.user:
        return render_template('market.html', paginates=paginates, name=g.user.name,img=g.user.img)
    return render_template('market.html',paginates=paginates)


@blue.route("/sortgoods/")
def sortGoods():
    page = int(request.args.get("page") or 1)
    type = request.args.get("type")
    try:
        type = type.split("/")[0]
        cache.set("type",type)
    except:
        type = cache.get("type")
        pass
    print(type)
    per = 12
    paginates = Goods.query.filter(Goods.type == type).paginate(page, per)
    if g.user:
        return render_template('market.html',type=type,paginates=paginates, name=g.user.name,img=g.user.img)
    return render_template("sort.html",paginates=paginates,type=type)



@blue.route("/register/",methods=["POST"])
def register():
    user = User()
    # request.form.get()
    user.name = "测试---"+str(random.randrange(100,1000))
    if request.args.get("name"):
        user.name=request.args.get("name")
    user.passwd = request.form.get("passwd")
    user.email = request.form.get("email")
    # user.img = "static/img/0.jpg"
    img = request.files.get("header")
    print(img.filename)
    img.save('app/static/img/header/'+img.filename)
    user.img = "img/header/"+img.filename
    user.token = str(uuid.uuid5(uuid.uuid4(),"h"))
    db.session.add(user)
    db.session.commit()
    session["token"] = user.token
    return redirect(url_for("bp.index"))



@blue.route("/login/",methods=["POST","GET"])
def login():
    email = request.args.get("email")
    passwd = request.args.get("passwd")
    print(email)
    print(passwd)
    user = User.query.filter(User.passwd == passwd).filter(User.email == email).first()
    if request.method=='GET':
        if user:
            return jsonify({"msg":1})
        else:
            return jsonify({"msg":0})

    email = request.form.get("email")
    passwd = request.form.get("passwd")
    user = User.query.filter(User.passwd == passwd).filter(User.email == email).first()
    user.token = str(uuid.uuid5(uuid.uuid4(),"p"))
    db.session.add(user)
    db.session.commit()
    session["token"] = user.token
    return redirect(url_for("bp.index"))



@blue.route("/logout/")
def logout():
    session.pop("token")
    return redirect(url_for("bp.index"))

@blue.before_request
def before():
    token = session.get("token")
    try:
        user = User.query.filter(User.token==token)[0]
    except:
        user = None
    g.user = user


@blue.route("/addtocart/")
def addtocart():
    goodsid = request.args.get("goodsid")
    if g.user:
        cart = UserGoods.query.filter(UserGoods.u_goods==goodsid,UserGoods.u_user==g.user.id).first()
        if cart:
            cart.num+=1
        else:
            cart = UserGoods()
            cart.u_goods = goodsid
            cart.u_user = g.user.id
            cart.num=1
        db.session.add(cart)
        db.session.commit()
        return jsonify({"msg":1})
    else:
        return jsonify({"msg":0})


@blue.route("/checkemail/")
def checkemail():
    email = request.args.get("email")
    user = User.query.filter(User.email==email).first()
    if user:
        return jsonify({"msg":0})
    return jsonify({"msg":1})


@blue.route('/senderemail/')
def send_email():
    code = str(random.randrange(100000, 1000000))
    try:
        email = request.args.get("email")
        print(email)
        msg = Message(subject="注册验证",recipients=[email])
        # msg.html = "<h2>啦啦啦</h2>"
        # 这个 html是在template中写好的，只用写body部分
        msg.html = "<h2>{}</h2>".format(code)
        # 这个mail指的是在ext.py中初始化的mail
        mail.send(msg)
        return jsonify({"msg":"发送成功","code":code})
    except:
        return jsonify({"msg":"发送失败","code":code})

@blue.route("/mine/",methods=["GET",'POST'])
def mine():
    email = request.args.get("email")
    user = User.query.filter(User.email==email).first()
    if request.method=="POST":
        name = request.form.get("name")
        if name:
            user.name = name
        img = request.files.get("img")
        if img:
            img.save("app/static/img/header/"+img.filename)
            user.img="img/header/"+img.filename
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('bp.index'))

    return render_template("mine.html",name=g.user.name,img=g.user.img,email = g.user.email)

@blue.route("/minus/")
def minus():
    user = g.user
    goodid = int(request.args.get("goodid"))
    cart = UserGoods.query.filter(UserGoods.u_user==user.id,UserGoods.u_goods==goodid).first()
    cart.num -= 1
    if cart.num==0:
        db.session.delete(cart)
        db.session.commit()
    else:
        db.session.add(cart)
        db.session.commit()
    return jsonify({"msg":"ok","cart":cart.num})

@blue.route("/add/")
def add():
    user = g.user
    goodid = int(request.args.get("goodid"))
    cart = UserGoods.query.filter(UserGoods.u_user==user.id,UserGoods.u_goods==goodid).first()
    cart.num += 1
    db.session.add(cart)
    db.session.commit()
    return jsonify({"msg":"ok","cart":cart.num})









