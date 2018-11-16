import random
import uuid

from flask import Blueprint, render_template, url_for, session, request, redirect, g

from app.ext import db
from app.models import User
blue = Blueprint("bp",__name__)
def init_blue(app):
    app.register_blueprint(blueprint=blue)

@blue.route("/")
def index():
    # print(url_for("bp.addUser"))
    print(g.user)
    if g.user:
        return render_template("index.html",user = g.user)

@blue.route("/shopping/")
def shopping():
    return render_template("shopping.html")

@blue.route("/cart/")
def cart():
    return  render_template("cart.html")

@blue.route("/order/")
def order():
    return render_template("order.html")


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

@blue.before_request
def before():
    token = session.get("token")
    user = User.query.filter(User.token==token)
    if user:
        g.user = user






