from app.ext import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    token = db.Column(db.String(256))
    # u_usergoods = db.relationship("UserGoods",backref="user",lazy=True)
    email = db.Column(db.String(100))
    passwd = db.Column(db.String(100))
    img = db.Column(db.String(256))

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    img = db.Column(db.String(100))
    org_price = db.Column(db.String(30))
    price = db.Column(db.String(30))
    buy_num = db.Column(db.String(30))
    quan = db.Column(db.String(30))
    type = db.Column(db.String(30),default="男装")




# class Goods(db.Model):
#     id  = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(40))
#     detial = db.Column(db.String(256))
#     price = db.Column(db.Integer)
#     u_usergoods = db.relationship("UserGoods",backref="goods",lazy=True)
#
#
class UserGoods(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_goods = db.Column(db.Integer, db.ForeignKey(Goods.id,ondelete="CASCADE",onupdate="CASCADE"))
    u_user = db.Column(db.Integer, db.ForeignKey(User.id,ondelete="CASCADE",onupdate="CASCADE"))
    num = db.Column(db.Integer)