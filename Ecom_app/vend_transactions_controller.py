
from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session

@app.route('/vend/transactions/')
def vend_transactions():
    tran = Transaction.query.filter_by(vendId=session['vendid']).all()
    print(tran)
    return render_template('vend_transactions.html',msg=session['msg'],
                           usertype=session['utype'],
                           user=session['vendid'],
                           tran=tran)
