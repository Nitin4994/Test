
from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session


def give_fresh_product():
    products = []
    for onePrd in Product.query.all():
        oneInv = Inventory.query.filter_by(prodId=onePrd.prodId).first()
        if not oneInv:
            products.append(onePrd)
    return products

def give_vend_product():
    vendProducts = []
    for onePrd in Product.query.all():
        oneInv = Inventory.query.filter_by(prodId=onePrd.prodId,vendId=session['vendid']).first()
        if oneInv:
            vendProducts.append(onePrd)
    return vendProducts

@app.route('/inventory/')
def inventory():

    return render_template('inventory.html', msg=session['msg'], usertype=session['utype'],
                           products = give_fresh_product(),
                           vendProd = give_vend_product())


@app.route('/add/inventory/',methods=["POST"])
def add_inventory():
    product = Product.query.filter_by(prodId=request.form['prodid']).first()
    totAmount = product.prodQty * product.prodPrice
    afterDiscAmount = totAmount - (totAmount * 0.10)
    vend = Vendor.query.filter_by(vendId=session['vendid']).first()
    venacc = Account.query.filter_by(accNo=vend.vendAcc).first()
    vendBal = vend.accref.accBal
    print("Vend bal--",vendBal)

    admin = Vendor.query.filter_by(vendRole=101).first()
    adminBal = admin.accref.accBal
    print("Admin bal--",adminBal)

    if vendBal<totAmount:
        print('Unsufficient Balance')
        return render_template('inventory.html', msg=session['msg'], usertype=session['utype'],
                               products=give_fresh_product(),
                               vendProd=give_vend_product(),
                               msg2 = 'Unsufficient Balance')
    else:
        # venacc.accBal = venacc.accBal-afterDiscAmount
        # print("After Vend bal--", venacc.accBal)

        vend.accref.accBal = vend.accref.accBal - float(afterDiscAmount)
        admin.accref.accBal = admin.accref.accBal + float(afterDiscAmount)
        db.session.commit()
        print("After Vend bal--", vend.accref.accBal)
        print("After Admin bal--", admin.accref.accBal)

        invInfo = Inventory(prodId=product.prodId, vendId=session['vendid'], qty=product.prodQty, price=product.prodPrice,
                        totAmount=totAmount, afterDiscAmount=afterDiscAmount)
        print(invInfo)
        db.session.add(invInfo)
        db.session.commit()

        # Transaction of Vendor withdrawal
        traDescVend = 'Buying prod-{} from {}'.format(product.prodName,admin.vendName)
        print(traDescVend)
        tranvend = Transaction(vendId=vend.vendId, traDesc=traDescVend, withdrawal=afterDiscAmount,
                               totBal=vend.accref.accBal)
        print(tranvend)
        db.session.add(tranvend)
        db.session.commit()

        # Transaction of Admin Deposit
        traDescAdmin = 'Selling prod-{} to {}'.format(product.prodName, vend.vendName)
        print(traDescAdmin)
        tranAdmin = Transaction(vendId=admin.vendId, traDesc=traDescAdmin, deposit=afterDiscAmount,
                                totBal=admin.accref.accBal)
        print(tranAdmin)
        db.session.add(tranAdmin)
        db.session.commit()

        return render_template('inventory.html', msg=session['msg'], usertype=session['utype'],
                               products = give_fresh_product(),vendProd=give_vend_product(),
                               msg2 = 'Transaction Successful..')
