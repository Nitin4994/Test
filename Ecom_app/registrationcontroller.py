
from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session


@app.route('/user/registration/',methods=['GET','POST'])
def user_registration():
    if request.method=='POST':
        #print(request.form)
        accs = Account.query.all()
        # Account(accId=, accNo=, accName=, accBal= )
        accInfo = Account(accNo=100103301 + len(accs), accName=request.form['name'], accBal=125000)

        userinfo = UserInfo(userName=request.form['name'], userAge=request.form['age'],
                            userAddress=request.form['address'], userMobile=request.form['contactno'],
                            userActive='Yes')

        logininfo = LoginInfo(loginName=request.form['username'], password=request.form['password'])


        usernames = LoginInfo.query.all()
        for user in usernames:
            if user.loginName == request.form['username']:
                return render_template('registration.html', msg='User name is Duplicate..')

        if request.form['password'] != request.form['confirmpassword']:
            return render_template('registration.html',msg='Password and Confirm Password not match')

        db.session.add(accInfo)
        db.session.commit()

        userinfo.userAcc=accInfo.accNo
        db.session.add(userinfo)
        db.session.commit()

        logininfo.uId = userinfo.id
        db.session.add(logininfo)
        db.session.commit()

        #role = Roles.query.filter_by(roleId=101).first()  #Admin
        #role = Roles.query.filter_by(roleId=102).first()  #vendor
        role = Roles.query.filter_by(roleId=103).first()  #user
        role.userrefs.append(userinfo)
        db.session.commit()

        # Transaction of User Deposit
        traDescUser = 'A/c Opening Deposit {}'.format(accInfo.accBal)
        print(traDescUser)
        # Transaction(traId=, vendId=, userId=, traDesc=, deposit=, withdrawal=, totBal=)
        tranUser = Transaction(userId=userinfo.id, traDesc=traDescUser, deposit=accInfo.accBal,
                               totBal=accInfo.accBal)
        print(tranUser)
        db.session.add(tranUser)
        db.session.commit()

        return render_template('login.html',msg='Register Successfull..!')
    else:
        return render_template('registration.html')