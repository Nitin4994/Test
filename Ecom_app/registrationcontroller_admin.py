

from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session

@app.route('/admin/home/')
def admin_home():
    return render_template('super_admin_dashbord.html',msg=session['msg'], usertype=session['utype'])



@app.route('/admin/registration/')
def admin_registration():
    return render_template('registration_admin.html',msg=session['msg'], usertype=session['utype'],
                           regrinfo = Vendor.query.all())


@app.route('/admin/registration/save/', methods=['GET','POST'])
def admin_save_registration():
    if request.method=='POST':
        #print(request.form)

        vends = Vendor.query.all()
        accs = Account.query.all()
        # Account(accId=, accNo=, accName=, accBal= )
        accInfo = Account(accNo=100103301 + len(accs), accName=request.form['name'], accBal=500000)


        role = Roles.query.filter_by(roleId=102).first()  # vendor
        vendinfo = Vendor(vendName=request.form['name'],vendAddress=request.form['address'],
                          vendContact=request.form['contactno'],vendActive='Yes',
                          vendRole=role.roleId)
        logininfo = LoginInfoVendor(vendLoginName=request.form['username'],
                                    vendPassword=request.form['password'])

        venderloginname = LoginInfoVendor.query.all()
        #print(venderloginname)
        for vendlogin in venderloginname:
            if vendlogin.vendLoginName == request.form['username']:
                return render_template('registration_admin.html',msg2='User name is Duplicate..',
                                       msg=session['msg'], usertype=session['utype'],
                                       regrinfo=Vendor.query.all())

        if request.form['password'] != request.form['confirmpassword']:
            return render_template('registration_admin.html',msg2='Password and Confirm Password not match',
                                   msg=session['msg'],usertype=session['utype'],
                                   regrinfo = Vendor.query.all())

        db.session.add(accInfo)
        db.session.commit()

        vendinfo.vendAcc=accInfo.accNo
        db.session.add(vendinfo)
        db.session.commit()

        logininfo.vId = vendinfo.vendId
        db.session.add(logininfo)
        db.session.commit()

        # Transaction of Vendor Deposit
        traDescVend = 'A/c Opening Deposit {}'.format(accInfo.accBal)
        print(traDescVend)
        # Transaction(traId=, vendId=, userId=, traDesc=, deposit=, withdrawal=, totBal=)
        tranVend = Transaction(vendId=vendinfo.vendId, traDesc=traDescVend, deposit=accInfo.accBal,
                                totBal=accInfo.accBal)
        print(tranVend)
        db.session.add(tranVend)
        db.session.commit()

        #return render_template('registration_admin.html',msg='Admin Register Successfull..!')
        return render_template('registration_admin.html', msg=session['msg'],usertype=session['utype'],
                               regrinfo = Vendor.query.all())
    else:
        return render_template('registration_admin.html', msg=session['msg'],usertype=session['utype'],
                               regrinfo = Vendor.query.all())