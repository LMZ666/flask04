import random
import uuid

from flask import Blueprint, render_template, url_for, session, request, redirect, g

from app.ext import db, cache
from app.models import User,Goods

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
        return render_template("index.html",name = g.user.name,wheels= wheels,classfiy=classfiy)
    return render_template("index.html",wheels= wheels,classfiy=classfiy)

@blue.route("/shopping/")
def shopping():
    return render_template("shopping.html")

@blue.route("/cart/")
def cart():
    return  render_template("cart.html")

@blue.route("/order/")
def order():
    return render_template("order.html")


@blue.route("/market/")
def market():
    page = int(request.args.get("page") or 1)
    per = 18
    paginates = Goods.query.paginate(page,per)
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
    return render_template("sort.html",paginates=paginates,type=type)



@blue.route("/register/",methods=["POST"])
def register():
    user = User()
    # request.form.get()
    user.name = "测试---"+str(random.randrange(100,1000))
    user.passwd = request.form.get("passwd")
    user.email = request.form.get("email")
    user.img = "static/img/0.jpg"
    user.token = str(uuid.uuid5(uuid.uuid4(),"h"))
    db.session.add(user)
    db.session.commit()
    session["token"] = user.token
    return redirect(url_for("bp.index"))



@blue.route("/login/",methods=["POST"])
def login():
    email = request.form.get("email")
    passwd = request.form.get("passwd")
    print(email)
    print(passwd)
    user = User.query.filter(User.passwd==passwd).filter(User.email==email).first()
    print(user)
    if user:
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







