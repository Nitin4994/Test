
from scoopn.Ecom_app.models import *
from flask import Flask,request,render_template,session

@app.route('/ecomapp/')
def first_loading_page():
    try:
        session.pop('utype')
        session.pop('msg')
        session.pop('userid')
        session.pop('vid')
    except:
        pass
    return render_template('login.html')

@app.route('/user/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #userinfo = request.form
        logininfo = LoginInfo.query.filter(LoginInfo.loginName==request.form['username'],
                                           LoginInfo.password==request.form['password']).first()
        logininfosuper = LoginInfoVendor.query.filter(LoginInfoVendor.vendLoginName==request.form['username'],
                                                      LoginInfoVendor.vendPassword==request.form['password']).first()

        if logininfo:
            user = UserInfo.query.filter_by(id=logininfo.uId).first()
            session['userid']=user.id
            session['msg']='Welcome {}'.format(user.userName)
            session['utype']=user.roleref.roleName
            vend = Vendor.query.all()
            return render_template('user_vender_selection.html', msg = session['msg'],
                                   usertype = session['utype'],user = session['userid'],
                                   username = user ,vendors = vend)
        elif logininfosuper:
            vend = Vendor.query.filter_by(vendId=logininfosuper.vId).first()
            session['msg']='Welcome {}'.format(vend.vendName)
            vendtype = Roles.query.filter_by(roleId=vend.vendRole).first()
            session['utype']=vendtype.roleName
            session['vendid'] = vend.vendId
            return render_template('super_admin_dashbord.html',vend=session['vendid'],
                                   msg=session['msg'],usertype=session['utype'])
        else:
            return render_template('login.html',msg='Invalid User Name or Password..')


if __name__ == '__main__':
    app.run(debug=True)