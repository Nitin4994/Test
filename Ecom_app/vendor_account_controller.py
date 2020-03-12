
from flask import Flask,session,request,render_template
from scoopn.Ecom_app.models import *

@app.route('/vendor/account/')
def vendor_account():
    return render_template('vendor_account.html', msg=session['msg'], usertype=session['utype'])