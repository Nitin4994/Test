
from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session

@app.route('/user/transactions/')
def user_transactions():
    user = UserInfo.query.filter_by(id=session['userid']).first()

    tran = Transaction.query.filter_by(userId=user.id).all()
    print(tran)
    return render_template('user_transactions.html',
                           get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                           usertype=session['utype'],
                           user=session['userid'],
                           username=user, tran=tran)