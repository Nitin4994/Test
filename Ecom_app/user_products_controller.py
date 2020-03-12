
from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session

def get_user_poducts():
    products = []
    invs = Inventory.query.filter_by(vendId=session['vid']).all()
    for inv in invs:
        prods = Product.query.filter_by(prodId=inv.prodId).first()
        products.append(prods)
    return products

def get_my_order():
    user_ords = OrderDetail.query.filter_by(userId=session['userid'],vendId=session['vid'],
                                            ordActive='Yes').all()
    return user_ords

def get_my_buy_order():
    user_ords = OrderDetail.query.filter_by(userId=session['userid'],vendId=session['vid'],
                                            ordActive='No').all()
    return user_ords

@app.route("/user/product/")
def user_product():
    user = UserInfo.query.filter_by(id=session['userid']).first()
    return render_template('user_products.html',
                           usertype=session['utype'],
                           user=session['userid'],
                           username = user,
                           get_vend = Vendor.query.filter_by(vendId=session['vid']).first(),
                           products = get_user_poducts(),
                           msg='',
                           myordprod = get_my_order(),
                           mybuyprod=get_my_buy_order())

@app.route("/user/product/add/", methods = ["GET","POST"])
def user_poducts_add():
    if request.method=="POST":
        print(request.form)
        user = UserInfo.query.filter_by(id=session['userid']).first()

        prodPrice = Product.query.filter_by(prodId=request.form['product']).first()
        ord = OrderDetail(userId=session['userid'],
                          vendId=session['vid'],
                          prodId=request.form['product'],
                          qty=request.form['prodqty'],
                          price=prodPrice.prodPrice)
        db.session.add(ord)
        db.session.commit()


        return render_template('user_products.html',
                               usertype=session['utype'], user=session['userid'],
                               get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                               username=user,
                               products = get_user_poducts(),
                               myordprod = get_my_order(),
                               mybuyprod=get_my_buy_order())