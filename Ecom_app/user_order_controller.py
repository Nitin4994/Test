
from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session
from scoopn.Ecom_app.user_products_controller import *

@app.route("/user/order/")
def user_orders():
    user = UserInfo.query.filter_by(id=session['userid']).first()
    return render_template('user_order.html',
                           get_vend = Vendor.query.filter_by(vendId=session['vid']).first(),
                           usertype=session['utype'],
                           user=session['userid'],
                           username=user,
                           msg='',
                           myordprod=get_my_order(),
                           mybuyprod=get_my_buy_order())