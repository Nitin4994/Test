

from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session

@app.route("/product/")
def product():
    return render_template('product.html',msg=session['msg'],usertype=session['utype'],
                           prod=Product.query.all())

@app.route("/add/product/",methods=["POST"])
def add_update_product():
    reqprod = request.form
    # Product(prodId=,prodName=,prodCategory=,prodQty=,prodPrice=,prodActive=)
    getprod = Product.query.filter_by(prodName=reqprod['prodname']).first()
    if getprod:
        getprod.prodName = reqprod['prodname']
        getprod.prodCategory = reqprod['prodcat']
        getprod.prodQty = reqprod['prodqty']
        getprod.prodPrice = reqprod['prodprice']
        getprod.prodActive = 'Yes'
        msg2='Product Updated..'
    else:
        prod = Product(prodName=reqprod['prodname'], prodCategory=reqprod['prodcat'],
                       prodQty=reqprod['prodqty'], prodPrice=reqprod['prodprice'],
                       prodActive = 'Yes')
        db.session.add(prod)
        msg2 = 'Product Inserted..'
    db.session.commit()

    return render_template('product.html', msg2=msg2, msg=session['msg'], usertype=session['utype'],
                           prod=Product.query.all())

