
import time

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Nitin4994@localhost/ecomapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY'] = 'JDHGTEU76HSGW5SHSKW82SDF'
db = SQLAlchemy(app)

user_role = db.Table('user_role',
    db.Column('u_id',db.ForeignKey("user_info.user_id"),primary_key=True),
    db.Column('r_id',db.ForeignKey("roles.role_id"),primary_key=True))

class UserInfo(db.Model):
    id = db.Column('user_id', db.Integer(), primary_key=True)
    userName = db.Column('user_nm', db.String(50))
    userAge = db.Column('user_age', db.Integer())
    userAddress = db.Column('user_add', db.String(50))
    userMobile = db.Column('user_mob', db.BigInteger())
    userActive =  db.Column('user_active', db.String(50))
    userAcc = db.Column('user_acc_no', db.ForeignKey('account.acc_no'),
                        unique=True, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(),
                           server_onupdate=db.func.now())
    loginref = db.relationship("LoginInfo", backref="userinforef", lazy=True, uselist=False)
    travendref = db.relationship("Transaction", backref="userinforef", lazy=True, uselist=True)

#Userinformation(id=,userName=,userAge=,userAddress=,userMobile=,userActive=,userAcc=)

class LoginInfo(db.Model):
    loginId = db.Column('login_id', db.Integer(), primary_key=True)
    loginName = db.Column('login_nm', db.String(50),unique=True)
    password = db.Column('password', db.String(50))
    uId = db.Column('u_id', db.ForeignKey("user_info.user_id"), unique=True, nullable=False)

#LoginInformation(loginName=, password=, uId=)


class Roles(db.Model):
    roleId = db.Column('role_id',db.Integer(),primary_key=True)
    roleName = db.Column('role_name',db.String(50))
    userrefs = db.relationship("UserInfo", secondary=user_role,
                               backref=db.backref("roleref", lazy=True, uselist=False))

class Vendor(db.Model):
    vendId = db.Column('vend_id', db.Integer(), primary_key=True)
    vendName = db.Column('vend_name', db.String(50))
    vendAddress = db.Column('vend_address', db.String(50))
    vendContact = db.Column('vend_contact', db.BigInteger())
    vendActive = db.Column('vend_active', db.String(50))
    vendRole = db.Column('vend_role_id', db.ForeignKey('roles.role_id'), unique=False, nullable=False)
    vendAcc = db.Column('vend_acc_no', db.ForeignKey('account.acc_no'), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    vendinvrefs = db.relationship("Inventory",backref="vendref", lazy=True, uselist=True)
    travendref = db.relationship("Transaction", backref="vendref", lazy=True, uselist=True)

#Vendor(vendId=,vendName=,vendAddress=,vendContact=,vendActive=,vendRole=,vendAcc=)

class LoginInfoVendor(db.Model):
    vendLoginId = db.Column('login_id', db.Integer(), primary_key=True)
    vendLoginName = db.Column('login_nm', db.String(50),unique=True)
    vendPassword = db.Column('password', db.String(50))
    vId = db.Column('v_id', db.ForeignKey("vendor.vend_id"), unique=True, nullable=False)

#LoginInfoVendor(vendLoginName=,vendPassword=,vId=)

class Account(db.Model):
    accId = db.Column('acc_id',db.Integer(),primary_key=True)
    accNo = db.Column('acc_no',db.BigInteger(),unique=True)
    accName = db.Column('acc_name', db.String(50))
    accBal = db.Column('acc_bal', db.Float())
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    vendref = db.relationship("Vendor", backref="accref", lazy=True, uselist=True)

#Account(accId=, accNo=, accName=, accBal= )

class Product(db.Model):
    prodId = db.Column('prod_id',db.Integer(),primary_key=True)
    prodName = db.Column('prod_name', db.String(50),unique=True)
    prodCategory = db.Column('prod_cat', db.String(50))
    prodPrice = db.Column('prod_price', db.Float())
    prodQty = db.Column('prod_qty', db.Integer())
    prodActive = db.Column('prod_active', db.String(50),default = 'Yes')
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    invvendrefs = db.relationship("Inventory",backref="prodref", lazy=True, uselist=True)

#Product(prodId=,prodName=,prodCategory=,prodQty=,prodPrice=,prodActive=)

class Inventory(db.Model):
    invtId = db.Column('invt_id',db.Integer(),primary_key=True)
    prodId = db.Column('prod_id', db.ForeignKey("product.prod_id"), unique=True, nullable=False)
    vendId = db.Column('vend_id', db.ForeignKey("vendor.vend_id"), unique=False, nullable=False)
    qty = db.Column('prod_qty', db.Integer())
    price = db.Column('prod_price', db.Float())
    totAmount = db.Column('total_amount', db.Float())
    afterDiscAmount = db.Column('aft_dis_amt', db.Float())
    invActive = db.Column('pur_active', db.String(10), default='Yes')
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

#Inventory(invtId=, prodId=, vendId=, qty=, price=, totAmount=, afterDiscAmount=,invActive=)

class OrderDetail(db.Model):
    ordId = db.Column('ord_id',db.Integer(),primary_key=True)
    userId = db.Column('user_id', db.ForeignKey("user_info.user_id"), unique=False, nullable=False)
    vendId = db.Column('vend_id', db.ForeignKey("vendor.vend_id"), unique=False, nullable=False)
    prodId = db.Column('prod_id', db.ForeignKey("product.prod_id"), unique=False, nullable=False)
    qty = db.Column('prod_qty', db.Integer())
    price = db.Column('prod_price', db.Float())
    ordActive = db.Column('ord_active', db.String(10), default='Yes')
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

#OrderDetail(userId=,vendId=,prodId=,qty=,price=,ordActive=)

class Purchase(db.Model):
    purId = db.Column('pur_id', db.Integer(), primary_key=True)
    userId = db.Column('user_id', db.ForeignKey("user_info.user_id"), unique=False, nullable=False)
    vendId = db.Column('vend_id', db.ForeignKey("vendor.vend_id"), unique=False, nullable=False)
    prodId = db.Column('prod_id', db.ForeignKey("product.prod_id"), unique=False, nullable=False)
    qty = db.Column('prod_qty', db.Integer())
    price = db.Column('prod_price', db.Float())
    totAmount = db.Column('total_amount', db.Float())
    afterDiscAmount = db.Column('aft_dis_amt', db.Float())
    purActive = db.Column('pur_active', db.String(10), default='Yes')
    purrefund = db.Column('pur_refund', db.String(10), default='No')
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

#Purchase(purId=,userId=,vendId=,prodId=,qty=,price=,totAmount=,afterDiscAmount=,purActive=,purrefund=)

class Transaction(db.Model):
    traId = db.Column('tra_id',db.Integer(),primary_key=True)
    vendId = db.Column('vend_id', db.ForeignKey("vendor.vend_id"), unique=False, nullable=True)
    userId = db.Column('user_id', db.ForeignKey("user_info.user_id"), unique=False, nullable=True)
    traDesc = db.Column('tra_description',db.String(500))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    deposit = db.Column('deposite',db.Float())
    withdrawal = db.Column('withdrawal',db.Float())
    totBal = db.Column('tot_bal', db.Float())
#Transaction(traId=, vendId=, userId=, traDesc=, deposit=, withdrawal=, totBal=)

if __name__ == '__main__':
    db.drop_all()
    print('Drop all..')
    time.sleep(2)
    db.create_all()
    print('Create all..')

    r1 = Roles(roleId=101,roleName='Admin')
    r2 = Roles(roleId=102, roleName='Vendor')
    r3 = Roles(roleId=103, roleName='User')
    db.session.add_all([r1,r2,r3])
    db.session.commit()
    print('Roles added..')

    accs = Account.query.all()
    accInfo = Account(accNo=100103301 + len(accs), accName='Admin', accBal=100000)
    db.session.add(accInfo)
    db.session.commit()
    print(accInfo.accId, accInfo.accNo, accInfo.accName, accInfo.accBal)

    v1 = Vendor(vendName='Admin', vendAddress='Pune', vendContact=8899768989,vendActive='Yes',
                vendRole=r1.roleId,vendAcc=accInfo.accNo)
    db.session.add(v1)
    db.session.commit()

    vlogin1 = LoginInfoVendor(vendLoginName=v1.vendName,vendPassword='super@123',vId=v1.vendId)
    db.session.add(vlogin1)
    db.session.commit()
    print('Vendor added..')

    # Transaction of Admin Deposit
    traDescAdmin = 'A/c Opening Deposit {}'.format(accInfo.accBal)
    print(traDescAdmin)
    # Transaction(traId=, vendId=, userId=, traDesc=, deposit=, withdrawal=, totBal=)
    tranAdmin = Transaction(vendId=v1.vendId, traDesc=traDescAdmin, deposit=accInfo.accBal,
                            totBal=accInfo.accBal)
    print(tranAdmin)
    db.session.add(tranAdmin)
    db.session.commit()