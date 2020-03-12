
from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session

@app.route("/user/dashbord/<int:vid>")
def vendor_product(vid):
    session['vid'] = vid
    user = UserInfo.query.filter_by(id=session['userid']).first()
    return render_template('user_dashbord.html',
                           get_vend = Vendor.query.filter_by(vendId=session['vid']).first(),
                           usertype=session['utype'], user=session['userid'],
                           username = user,msg='')

