
from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session

@app.route('/user/purchase/<int:oid>')
def user_purchase(oid):
    # OrderDetail(userId=,vendId=,prodId=,qty=,price=)
    allord = OrderDetail.query.all()
    ord = OrderDetail.query.filter_by(ordId=oid).first()
    user = UserInfo.query.filter_by(id=session['userid']).first()
    vend = Vendor.query.filter_by(vendId=ord.vendId).first()
    prod = Product.query.filter_by(prodId=ord.prodId).first()

    finalPrice = ord.qty * ord.price

    if finalPrice > 100000:
        discount = finalPrice * 0.05
        disfinalPrice = finalPrice - discount
        return render_template('user_purchase.html',
                               get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                               usertype=session['utype'],
                               user=session['userid'],
                               username=user,
                               vend=vend,
                               prod=prod,
                               ord=ord,
                               allord = allord,
                               finalPrice = finalPrice,
                               discount = discount,
                               disfinalPrice = disfinalPrice,
                               page=1)
    else:
        return render_template('user_purchase.html',
                               get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                               usertype=session['utype'],
                               user=session['userid'],
                               username=user,
                               vend=vend,
                               prod=prod,
                               ord=ord,
                               allord=allord,
                               finalPrice=finalPrice,
                               discount='No Discount',
                               disfinalPrice=finalPrice,
                               page=1)

@app.route('/user/purchase/place/<int:oid>')
def user_purchase_palce(oid):
    allord = OrderDetail.query.all()

    #OrderDetail(ordId=, userId=, vendId=, prodId=, qty=,price=)
    ord = OrderDetail.query.filter_by(ordId=oid).first()

    #Userinformation(id=,userName=,userAge=,userAddress=,userMobile=,userActive=,userAcc=)
    user = UserInfo.query.filter_by(id=session['userid']).first()

    # Account(accId=, accNo=, accName=, accBal= )
    userAcc = Account.query.filter_by(accNo=user.userAcc).first()

    #Vendor(vendId=,vendName=,vendAddress=,vendContact=,vendActive=,vendRole=,vendAcc=)
    vend = Vendor.query.filter_by(vendId=ord.vendId).first()
    vendAcc = Account.query.filter_by(accNo=vend.vendAcc).first()

    #Product(prodId=,prodName=,prodCategory=,prodQty=,prodPrice=,prodActive=)
    prod = Product.query.filter_by(prodId=ord.prodId).first()

    finalPrice = ord.qty * ord.price
    if ord.vendId==vend.vendId:
        if ord.prodId==prod.prodId:
            if ord.qty<=prod.prodQty:
                if userAcc.accBal >= finalPrice:
                    if finalPrice>100000:
                        #finalPrice = finalPrice - finalPrice * (5/100)  #Dis is 5%
                        #disfinalPrice = finalPrice - finalPrice * 0.05     #Dis is 5%  #Both lines are same
                        discount = finalPrice * 0.05
                        disfinalPrice = finalPrice - discount

                        prod.prodQty -= ord.qty
                        userAcc.accBal -= float(finalPrice)
                        vendAcc.accBal += float(finalPrice)

                        # Purchase(purId=,userId=,vendId=,prodId=,qty=,price=,totAmount=,afterDiscAmount=,purActive=,purrefund=)
                        purcOrd = Purchase(userId=user.id,
                                           vendId=vend.vendId,
                                           prodId=prod.prodId,
                                           qty=ord.qty,
                                           price=ord.price,
                                           totAmount=finalPrice,
                                           afterDiscAmount=disfinalPrice)
                        db.session.add(purcOrd)
                        db.session.commit()

                        #OrderDetail(userId=,vendId=,prodId=,qty=,price=,ordActive=)
                        ord.ordActive = 'No'
                        db.session.commit()

                        # Transaction(traId=, vendId=, userId=, traDesc=, deposit=, withdrawal=, totBal=)
                        # Transaction of user withdrawal
                        traDescUsr = 'Buying prod-{} from {}'.format(prod.prodName, vend.vendName)
                        print(traDescUsr)
                        tranUser = Transaction(userId=user.id, traDesc=traDescUsr, withdrawal=disfinalPrice,
                                               totBal=userAcc.accBal)
                        print(tranUser)
                        db.session.add(tranUser)
                        db.session.commit()

                        # Transaction of Vendor Deposit
                        traDescVend = 'Selling prod-{} to {}'.format(prod.prodName, user.userName)
                        print(traDescVend)
                        tranVend = Transaction(vendId=vend.vendId, traDesc=traDescVend, deposit=disfinalPrice,
                                               totBal=vendAcc.accBal)
                        print(tranVend)
                        db.session.add(tranVend)
                        db.session.commit()

                        return render_template('user_purchase.html',
                                               msg='After Discount Product is Sold..',
                                               get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                                               usertype=session['utype'],
                                               user=session['userid'],
                                               username=user,
                                               vend=vend,
                                               prod=prod,
                                               ord=ord,
                                               allord=allord,
                                               finalPrice=finalPrice,
                                               discount=discount,
                                               disfinalPrice=disfinalPrice,
                                               page = 2)
                    else:
                        prod.prodQty -= ord.qty
                        userAcc.accBal -= float(finalPrice)
                        vendAcc.accBal += float(finalPrice)

                        purcOrd = Purchase(userId=user.id,
                                           vendId=vend.vendId,
                                           prodId=prod.prodId,
                                           qty=ord.qty,
                                           price=ord.price,
                                           totAmount=finalPrice,
                                           afterDiscAmount=finalPrice)
                        db.session.add(purcOrd)
                        db.session.commit()

                        # OrderDetail(userId=,vendId=,prodId=,qty=,price=,ordActive=)
                        ord.ordActive = 'No'
                        db.session.commit()

                        # Transaction(traId=, vendId=, userId=, traDesc=, deposit=, withdrawal=, totBal=)
                        # Transaction of user withdrawal
                        traDescUsr = 'Buying prod-{} from {}'.format(prod.prodName, vend.vendName)
                        print(traDescUsr)
                        tranUser = Transaction(userId=user.id, traDesc=traDescUsr, withdrawal=finalPrice,
                                               totBal=userAcc.accBal)
                        print(tranUser)
                        db.session.add(tranUser)
                        db.session.commit()

                        # Transaction of Vendor Deposit
                        traDescVend = 'Selling prod-{} to {}'.format(prod.prodName, user.userName)
                        print(traDescVend)
                        tranVend = Transaction(vendId=vend.vendId, traDesc=traDescVend, deposit=finalPrice,
                                               totBal=vendAcc.accBal)
                        print(tranVend)
                        db.session.add(tranVend)
                        db.session.commit()

                        return render_template('user_purchase.html',
                                               msg='Product is Sold..',
                                               get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                                               usertype=session['utype'],
                                               user=session['userid'],
                                               username=user,
                                               vend=vend,
                                               prod=prod,
                                               ord=ord,
                                               allord=allord,
                                               finalPrice=finalPrice,
                                               discount='No Discount',
                                               disfinalPrice=finalPrice,
                                               page=2)
                else:
                    return render_template('user_purchase.html',
                                           msg='Unsufficient Balance..',
                                           get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                                           usertype=session['utype'],
                                           user=session['userid'],
                                           username=user,
                                           vend=vend,
                                           prod=prod,
                                           ord=ord,
                                           allord=allord,
                                           finalPrice=finalPrice,
                                           discount='No Discount',
                                           disfinalPrice=finalPrice,
                                           page=2)
            else:
                return render_template('user_purchase.html',
                                       msg='Out of Stock',
                                       get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                                       usertype=session['utype'],
                                       user=session['userid'],
                                       username=user,
                                       vend=vend,
                                       prod=prod,
                                       ord=ord,
                                       allord=allord,
                                       finalPrice=finalPrice,
                                       discount='No Discount',
                                       disfinalPrice=finalPrice,
                                       page=2)
        else:
            return render_template('user_purchase.html',
                                   msg='Product is unavailable',
                                   get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                                   usertype=session['utype'],
                                   user=session['userid'],
                                   username=user,
                                   vend=vend,
                                   prod=prod,
                                   ord=ord,
                                   allord=allord,
                                   finalPrice=finalPrice,
                                   discount='No Discount',
                                   disfinalPrice=finalPrice,
                                   page=2)
    else:
        return render_template('user_purchase.html',
                               msg='Vendor is unavailable',
                               get_vend=Vendor.query.filter_by(vendId=session['vid']).first(),
                               usertype=session['utype'],
                               user=session['userid'],
                               username=user,
                               vend=vend,
                               prod=prod,
                               ord=ord,
                               allord=allord,
                               finalPrice=finalPrice,
                               discount='No Discount',
                               disfinalPrice=finalPrice,
                               page=2)


